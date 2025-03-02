from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import shutil
import json
import webbrowser
from datetime import datetime
import subprocess  # Import subprocess module

# Flask app configuration
app = Flask(__name__)

# Constants
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ics'}
app.config['JSON_FOLDER'] = 'json'
URL = 'https://planmy.work/'
# URL = "http://127.0.0.1:5000/"

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
    # Call create_schedule.py
    subprocess.run(["python", "create_schedule.py"], check=True)
    
    # Read the contents of summary.txt
    summary_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'summary.txt')
    summary_content = ""
    if os.path.exists(summary_file_path):
        with open(summary_file_path, 'r') as summary_file:
            summary_content = summary_file.read()
    
    return render_template('results.html', filename=filename, summary_content=summary_content)

if __name__ == '__main__':
    ensure_folders_exist()
    clear_upload_folder()
    # webbrowser.open(URL)
    app.run(debug=True, host="0.0.0.0")
