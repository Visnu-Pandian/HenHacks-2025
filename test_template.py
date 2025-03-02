from google import genai
import os
from dotenv import load_dotenv
from generate import generate_ics_and_explanation, generate_prompt
import json

load_dotenv()
apiKey = os.getenv('API_KEY')
geminiModel = os.getenv('MODEL')

client = genai.Client(api_key=apiKey)

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def merge_schedules(task_schedule, input_schedule):
    merged_schedule = {
        "calendarSettings": {
            "dayStartTime": task_schedule["calendarSettings"]["dayStartTime"],
            "dayEndTime": task_schedule["calendarSettings"]["dayEndTime"],
            "blockedHours": input_schedule["calendarSettings"]["blockedHours"]
        },
        "tasks": task_schedule["tasks"] + input_schedule["tasks"],
        "filename": "merged_schedule.json"
    }
    return merged_schedule



task_schedule_path = 'json/task_schedule.json'
input_schedule_path = 'json/input_schedule.json'
merged_schedule_path = 'json/merged_schedule.json'

task_schedule = load_json(task_schedule_path)
input_schedule = load_json(input_schedule_path)

merged_schedule = merge_schedules(task_schedule, input_schedule)

save_json(merged_schedule, merged_schedule_path)
print(f'Merged schedule saved to {merged_schedule_path}')

def process_kwargs(**kwargs):
    """Replace falsy values in kwargs with 'None specified'."""
    return {key: value if value else "None specified" for key, value in kwargs.items()}

# Example usage
kwargs = {
    "tasks_str": "\n".join(
        [f"* Title: {task['title']}\n\t  Description: {task['description']}\n\t Start Time: {task["start_date"] if task["start_date"] else "None specified"}\n\t End Time: {task["end_date"] if task["end_date"] else "None specified"}\n\t Duration: {task['duration']} minutes\n\t Quantity: {task['quantity']}\n\t Time Preference: {task['timePreference']}" for task in merged_schedule["tasks"]]),
    "start_date": "Sunday, March 2, 2025",
    "end_date": "Saturday, March 8, 2025",
    "blocked_str": "\n".join([f"* Start: {block['startTime']}\n\t  End: {block['endTime']}" for block in merged_schedule["calendarSettings"]["blockedHours"]]),
    "timezone": "EST",
    "waking_start": merged_schedule["calendarSettings"]["dayStartTime"],
    "waking_end": merged_schedule["calendarSettings"]["dayEndTime"],
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