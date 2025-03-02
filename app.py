from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import shutil
import json
import webbrowser
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ics'}
app.config['JSON_FOLDER'] = 'json'
URL = 'https://planmy.work/'
# URL = "http://127.0.0.1:5000/"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

def clear_upload_folder():
    clear_folder(app.config['UPLOAD_FOLDER'])
    clear_folder(app.config['JSON_FOLDER'])

def ensure_folders_exist():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['JSON_FOLDER']):
        os.makedirs(app.config['JSON_FOLDER'])

def get_chars_after(text, char, num_chars):
    index = text.index(char)
    if index == -1 or index + len(char) + num_chars > len(text):
        return ""
    return text[index + len(char):index + len(char) + num_chars]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return redirect(request.url)

@app.route('/tasks/<filename>')
def tasks(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return redirect(url_for('index'))

    events = {
        'calendarSettings': {
            'dayStartTime': '00:00',
            'dayEndTime': '23:59',
            'blockedHours': [{'startTime': '23:59', 'endTime': '00:00'}]
        },
        'tasks': [],
        'filename': 'input.ics'
    }
    
    f = open(file_path, 'r')
    while True:
        line = f.readline()
        if line.startswith("DTSTART"):
            start_date = datetime.strptime(get_chars_after(line, ":", 15), '%Y%m%dT%H%M%S')
            if start_date < datetime(2025, 6, 9):
                break
            line = f.readline()
            end_date = datetime.strptime(get_chars_after(line, ":", 15), '%Y%m%dT%H%M%S')
            if end_date > datetime(2025, 6, 15):
                break
            duration = end_date - start_date
            while line.startswith("DESCRIPTION") == False:
                line = f.readline()
            description = line.split(":", 1)[1]
            while line.startswith("SUMMARY") == False:
                line = f.readline()
            summary = line.split(":", 1)[1]
            
            event = {
                'title': summary,
                'description': description,
                'duration': str(duration),
                'quantity': str(1),
                'timePreference': 'morning'
            }
            print(event)
            events['tasks'].append(event)
            
        else:
            continue
        
    f.close()

    # Convert events to JSON
    events_json = json.dumps(events, indent=4)
    
    filename = 'input_schedule.json'
    json_folder = app.config['JSON_FOLDER']
    os.makedirs(json_folder, exist_ok=True)
    file_path = os.path.join(json_folder, filename)
    
    with open(file_path, 'w') as json_file:
        json.dump(events, json_file)
        
    print(f'Events saved to {file_path}')
    print(events_json)
    
    return render_template('tasks.html', filename=filename, events=events)

@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    schedule = request.get_json()
    filename = 'task_schedule.json'
    json_folder = app.config['JSON_FOLDER']
    os.makedirs(json_folder, exist_ok=True)
    file_path = os.path.join(json_folder, filename)
    
    # Save the schedule to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(schedule, json_file)
    
    print(f'Schedule saved to {file_path}')
    print(schedule)
    
    # Assuming the save operation is successful, return a success response
    return jsonify({"status": "success", "filename": filename}), 200

@app.route('/results/<filename>')
def results(filename):
    return render_template('results.html', filename=filename)

if __name__ == '__main__':
    ensure_folders_exist()
    clear_upload_folder()
    webbrowser.open(URL)
    app.run(debug=True)
