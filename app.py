from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import shutil
import json
import webbrowser
from datetime import datetime
# import subprocess  # Import subprocess module
from google import genai
from dotenv import load_dotenv
from generate import *
from create_schedule import *
# Flask app configuration
app = Flask(__name__)

# Constants

app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ics'}
app.config['JSON_FOLDER'] = 'json'


# URL = 'https://planmy.work/'
URL = "http://127.0.0.1:5000/"


# Configure allowed filetypes
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Clear the contents of a folder
def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Clear the contents of the upload, download and json folders
def clear_upload_folder():
    clear_folder(app.config['UPLOAD_FOLDER'])
    clear_folder(app.config['JSON_FOLDER'])
    clear_folder(app.config['DOWNLOAD_FOLDER'])

# Ensure that the upload, download and json folders exist, create them if needed
def ensure_folders_exist():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['JSON_FOLDER']):
        os.makedirs(app.config['JSON_FOLDER'])
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])

# Custom helper method for .ics parsing
def get_chars_after(text, char, num_chars):
    index = text.index(char)
    if index == -1 or index + len(char) + num_chars > len(text):
        return ""
    return text[index + len(char):index + len(char) + num_chars]

# Render frontend html page
@app.route('/')
def index():
    return render_template('index.html')

# Upload file on submit button click
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        # Save the uploaded file to the uploads folder
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return redirect(request.url)

# Render tasks page with parsed events
@app.route('/tasks/<filename>')
def tasks(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return redirect(url_for('index'))

    # Create template for JSON file
    events = {
        'calendarSettings': {
            'dayStartTime': '00:00',
            'dayEndTime': '23:59',
            'blockedHours': [{'startTime': '23:59', 'endTime': '00:00'}]
        },
        'tasks': [],
        'filename': 'input.ics'
    }
    
    # Parse the .ics file
    f = open(file_path, 'r')
    print("Parsing file...")
    while True:
        # While loop to iterate through the file
        line = f.readline()
        if not line:
            break
        # Find the start of an event
        if line.startswith("BEGIN:VEVENT"):
            line = f.readline()
            # Parse start date
            if line.startswith("DTSTART"):
                start_date = datetime.strptime(get_chars_after(line, ":", 15), '%Y%m%dT%H%M%S')
                if start_date < datetime(2025, 3, 2):
                    break
                line = f.readline()
                # Parse end date
                end_date = datetime.strptime(get_chars_after(line, ":", 15), '%Y%m%dT%H%M%S')
                if end_date > datetime(2025, 3, 8):
                    break
                # Calculating task duration based on start and end date
                duration = end_date - start_date
                # Keep reading unil next decription task is found.
                while line.startswith("DESCRIPTION") == False:
                    line = f.readline()
                description = line.split(":", 1)[1]
                # Keep reading until next summary task is found.
                while line.startswith("SUMMARY") == False:
                    line = f.readline()
                summary = line.split(":", 1)[1]
            
                # Compliing the JSON object for the event
                event = {
                    'title': summary,
                    'description': description,
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'duration': str(duration),
                    'quantity': str(1),
                    'timePreference': 'morning'
                }
            
                print(event)
                # Adding JSON object to the events file
                events['tasks'].append(event)
            
        else:
            continue
        
    f.close()
    print("file done parsing")
    # Convert events to JSON
    events_json = json.dumps(events, indent=4)
    
    # Creating file at path
    filename = 'input_schedule.json'
    json_folder = app.config['JSON_FOLDER']
    os.makedirs(json_folder, exist_ok=True)
    file_path = os.path.join(json_folder, filename)
    
    # Dumping JON object to file
    with open(file_path, 'w') as json_file:
        json.dump(events, json_file)
        
    print(f'Events saved to {file_path}')
    print(events_json)
    
    # Rendering the tasks page with the parsed events
    return render_template('tasks.html', filename=filename, events=events)

# Saves the schedule to a JSON file
@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    schedule = request.get_json()
    # Creating file at path
    filename = 'task_schedule.json'
    json_folder = app.config['JSON_FOLDER']
    os.makedirs(json_folder, exist_ok=True)
    file_path = os.path.join(json_folder, filename)
    
    # Dumping JSON object to file
    with open(file_path, 'w') as json_file:
        json.dump(schedule, json_file)
    
    print(f'Schedule saved to {file_path}')
    print(schedule)
    
    # Assuming the save operation is successful, return a success response
    return jsonify({"status": "success", "filename": filename}), 200

# Final results page
@app.route('/results/<filename>')
def results(filename):
    load_dotenv()
    apiKey = os.getenv('API_KEY')
    geminiModel = os.getenv('MODEL')
    client = genai.Client(api_key=apiKey)
    task_schedule_path = 'json/task_schedule.json'
    input_schedule_path = 'json/input_schedule.json'
    merged_schedule_path = 'json/merged_schedule.json'
    task_schedule = load_json(task_schedule_path)
    input_schedule = load_json(input_schedule_path)

    merged_schedule = merge_schedules(task_schedule, input_schedule)

    save_json(merged_schedule, merged_schedule_path)
    print(f'Merged schedule saved to {merged_schedule_path}')

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
    with open(r"downloads/prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt)

    ics_content, summary = generate_ics_and_explanation(client, geminiModel, prompt)
    if ics_content and summary:
        with open(r"downloads/schedule.ics", "w", encoding="utf-8") as f:
            f.write(ics_content)
        with open(r"downloads/summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        print(summary)
    else:
        if ics_content is None:
            print("Failed to generate .ics file.")
        if summary is None:
            print("Failed to generate explanation.")
        
    # Read the contents of summary.txt
    summary_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'summary.txt')
    summary_content = ""
    if os.path.exists(summary_file_path):
        with open(summary_file_path, 'r') as summary_file:
            summary_content = summary_file.read()
    
    return render_template('results.html', filename=filename, summary_content=summary_content)

@app.route('/downloads/schedule.ics')
def download_schedule():
    return send_from_directory(directory="downloads", path="schedule.ics", as_attachment=True)

if __name__ == '__main__':
    ensure_folders_exist()
    clear_upload_folder()
    # webbrowser.open(URL)
    app.run(debug=True, host="0.0.0.0")
