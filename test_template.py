from google import genai
import os
from dotenv import load_dotenv
from generate import generate_ics_and_explanation, generate_prompt
import json

load_dotenv()
apiKey = os.getenv('API_KEY')
geminiModel = os.getenv('MODEL')

client = genai.Client(api_key=apiKey)

def parse_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    tasks = data['tasks']
    blocked_hours = data['calendarSettings']['blockedHours']
    day_start_time = data['calendarSettings']['dayStartTime']
    day_end_time = data['calendarSettings']['dayEndTime']

    return tasks, blocked_hours, day_start_time, day_end_time

def process_kwargs(**kwargs):
    """Replace falsy values in kwargs with 'None specified'."""
    return {key: value if value else "None specified" for key, value in kwargs.items()}

# Parse JSON file
json_file_path = 'json/schedule.ics'
tasks, blocked_hours, day_start_time, day_end_time = parse_json(json_file_path)

# Example usage
kwargs = {
    "tasks_str": "\n".join([f"* Title: {task['title']}\n\t  Description: {task['description']}\n\t  Duration: {task['duration']} minutes\n\t Quantity: {task['quantity']}\n\t Time Preference: {task['timePreference']}" for task in tasks]),
    "start_date": "Sunday, June 09, 2025",
    "end_date": "Saturday, June 15, 2025",
    "blocked_str": "\n".join([f"* Start: {block['startTime']}\n\t  End: {block['endTime']}" for block in blocked_hours]),
    "timezone": "EST",
    "waking_start": day_start_time,
    "waking_end": day_end_time,
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