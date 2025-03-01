from flask import Flask, render_template, request, redirect, url_for
import os
import icalendar

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ics'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        return redirect(url_for('results', filename=filename))
    return redirect(request.url)

@app.route('/results/<filename>')
def results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'rb') as file:
        gcal = icalendar.Calendar.from_ical(file.read())
    
    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            event = {
                'summary': component.get('summary'),
                'dtstart': component.get('dtstart').dt,
                'dtend': component.get('dtend').dt,
                'location': component.get('location'),
                'description': component.get('description')
            }
            events.append(event)
    
    return render_template('results.html', filename=filename, events=events)

if __name__ == '__main__':
    app.run(debug=True)