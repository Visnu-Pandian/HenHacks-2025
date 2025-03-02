import json
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

def process_kwargs(**kwargs):
    """Replace falsy values in kwargs with 'None specified'."""
    return {key: value if value else "None specified" for key, value in kwargs.items()}