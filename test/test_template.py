from google import genai
import os
from dotenv import load_dotenv
import json
load_dotenv()
apiKey = os.getenv('API_KEY')
geminiModel = os.getenv('MODEL')

client = genai.Client(api_key=apiKey)
def generate_ics_and_explanation(model, prompt):
    """Generates an .ics file and explanation using Gemini."""

    response = client.models.generate_content(
        model=geminiModel,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "ics_file": {
                        "type": "string",
                        "description": "The generated .ics file content as a string."
                    },
                    "chain_of_thought": {
                        "type": "string",
                        "description": "A detailed explanation of the scheduling decisions made, including heuristic application and reasoning."
                    }
                },
                "required": ["ics_file", "chain_of_thought"]
            }
        },
    )

    try:
        # Access the response as a dictionary
        response_dict = response.candidates[0].content.parts[0].text
        response_data = json.loads(response_dict) #parse the json string

        ics_content = response_data["ics_file"]
        chain_of_thought = response_data["chain_of_thought"]

        return ics_content, chain_of_thought

    except (AttributeError, IndexError, json.JSONDecodeError, KeyError) as e:
        print(f"Error processing response: {e}")
        print(response) #Print the raw response to help debugging.
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(response)
        return None, None
"""
    **Tasks:** (Provide a list of tasks with the following details for each task)
    * Title (SUMMARY)
    * Description (DESCRIPTION)
    * Duration (or Start Time and End Time in ISO 8601 format, e.g., 2024-03-05T10:00:00Z)

    **Blocked Times:** (Provide a list of blocked time slots with the following details for each slot)
    * Start Time (DTSTART in ISO 8601 format)
    * End Time (DTEND in ISO 8601 format)
    * Description (Optional)

    **Free Time Slots:** (Provide a list of available free time slots with the following details for each slot)
    * Start Time (DTSTART in ISO 8601 format)
    * End Time (DTEND in ISO 8601 format)

    **Heuristics:** (Provide a list of rules for scheduling tasks, including prioritization, handling overlaps, and any other relevant criteria. Be as specific as possible. Examples:)
    * "Prioritize tasks with shorter durations."
    * "Schedule the most important tasks first."
    * "Avoid scheduling tasks during the afternoon if possible."
    * "Schedule tasks of similar types together."
    * "Try to distribute tasks evenly throughout the available free time."
    * "Avoid scheduling tasks that overlap with blocked times."

    **Time Zone:** (Specify the time zone for all provided dates and times, e.g., UTC, America/New_York)
"""

start_date = "Sunday, June 09, 2025"
end_date = "Saturday, June 15, 2025"

tasks = []
for i in range(1, 5):
    tasks.append({
        "Title": f"Task {i}",
        "Description": f"Description for Task {i}",
        "Duration": f"{i} hour",
    })
tasks_str = "\n".join([f"* Title: {task['Title']}\n\t  Description: {task['Description']}\n\t  Duration: {task['Duration']}" for task in tasks])
prompt = f"""
Generate an iCalendar (.ics) file representing a weekly schedule based on the following information:

I want this week to start from {start_date}, and end on {end_date}.

**Tasks:** (Provide a list of tasks with the following details for each task)
{tasks_str}

**Blocked Times:** (Provide a list of blocked time slots with the following details for each slot)
* Start Time: 2025-06-10T08:00:00Z
* End Time: 2025-06-10T09:00:00Z
* Description: Morning Meeting

Normal waking hours are from 08:00 to 22:00. Allot breaks and meals as needed.

Do not just stack all the tasks at the start of the day. Scatter them 
throughout the available time slots.

The time zone for all provided dates and times is EST.

**Heuristics:** (Provide a list of rules for scheduling tasks, including prioritization, handling overlaps, and any other relevant criteria. Be as specific as possible. Examples:)
* "Prioritize tasks with shorter durations."
* Leave "transition time" between tasks to avoid back-to-back scheduling. Ideally, they should be about 15 minutes, but use your best judgment.
**Output Requirements:**

1.  Generate a valid .ics file containing the scheduled tasks and blocked times.
2.  After generating the .ics file, provide a detailed "chain of thought" in markdown format (using bold and stuff when necessary) explaining your reasoning behind the scheduling decisions. This explanation should include:
* How you interpreted and applied each of the provided heuristics.
* The order in which you processed the tasks.
* Specific decisions made during the scheduling process, such as task placement and conflict resolution.
* Any limitations or challenges encountered during the process.
* Potential improvements to the schedule or heuristics.

Please ensure the .ics file is properly formatted and includes all necessary iCalendar properties (e.g., UID, DTSTAMP, VERSION, PRODID).
"""
ics_content, chain_of_thought = generate_ics_and_explanation(geminiModel, prompt)

if ics_content and chain_of_thought:
    with open(r"test-outputs\schedule.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    with open(r"test-outputs\chain_of_thought.md", "w", encoding="utf-8") as f:
        f.write(chain_of_thought)
    print(chain_of_thought)
else:
    if ics_content is None:
        print("Failed to generate .ics file.")
    if chain_of_thought is None:
        print("Failed to generate explanation.")