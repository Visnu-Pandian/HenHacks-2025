from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import shutil
import icalendar

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ics'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def clear_upload_folder():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

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
    return render_template('tasks.html', filename=filename)

@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    schedule = request.get_json()
    filename = schedule.get('filename', 'default_schedule.json')
    # Here you would save the schedule to a database or file
    # For demonstration, we'll just print it to the console
    print(schedule)
    
    # Assuming the save operation is successful, return a success response
    return jsonify({"status": "success", "filename": filename}), 200

@app.route('/results/<filename>')
def results(filename):
    return render_template('results.html', filename=filename)

if __name__ == '__main__':
    clear_upload_folder()
    app.run(debug=True)