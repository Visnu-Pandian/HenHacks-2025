from google import genai
import os
from dotenv import load_dotenv
from generate import generate_ics_and_explanation, generate_prompt

load_dotenv()
apiKey = os.getenv('API_KEY')
geminiModel = os.getenv('MODEL')

client = genai.Client(api_key=apiKey)

preference_array = ["Morning", "Afternoon", "Evening"]

tasks = []
for i in range(1, 5):
    tasks.append({
        "Title": f"Task {i}",
        "Description": f"Description for Task {i}",
        "Duration": f"{i % 4 + 1} hour",
        "Quantity": f"{i % 5 + 1} times,",
        "Time Preference": f"{preference_array[i % 3]}",
    })
blocked = []
for i in range(1, 5):
    blocked.append({
        "Start": f"2025-06-1{i}T{12+i}:00:00",
        "End": f"2025-06-1{i}T{13+i}:00:00",
    })
def process_kwargs(**kwargs):
    """Replace falsy values in kwargs with 'None specified'."""
    return {key: value if value else "None specified" for key, value in kwargs.items()}

# Example usage
kwargs = {
    "tasks_str": "\n".join([f"* Title: {task['Title']}\n\t  Description: {task['Description']}\n\t  Duration: {task['Duration']}\n\t Quantity: {task['Quantity']}\n\t Time Preference: {task['Time Preference']}" for task in tasks]),
    "start_date": "Sunday, June 09, 2025",
    "end_date": "Saturday, June 15, 2025",
    "blocked_str": "\n".join([f"* Start: {block['Start']}\n\t  End: {block['End']}" for block in blocked]),
    "timezone": "EST",
    "waking_start": "08:00",
    "waking_end": "22:00",
}
processed_kwargs = process_kwargs(**kwargs)

prompt = generate_prompt(**processed_kwargs)
with open(r"test/test-outputs/prompt.md", "w", encoding="utf-8") as f:
    f.write(prompt)

ics_content, chain_of_thought = generate_ics_and_explanation(client, geminiModel, prompt)
if ics_content and chain_of_thought:
    with open(r"test/test-outputs/schedule.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    with open(r"test/test-outputs/chain_of_thought.md", "w", encoding="utf-8") as f:
        f.write(chain_of_thought)
    print(chain_of_thought)
else:
    if ics_content is None:
        print("Failed to generate .ics file.")
    if chain_of_thought is None:
        print("Failed to generate explanation.")