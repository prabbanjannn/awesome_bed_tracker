import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this'

BEDS_FILE = 'beds.json'

def load_beds():
    try:
        with open(BEDS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default = {"ICU": {"available": 0, "max": 20, "last_updated": str(datetime.now())},
                   "General": {"available": 0, "max": 50, "last_updated": str(datetime.now())},
                   "Oxygen": {"available": 0, "max": 30, "last_updated": str(datetime.now())}}
        save_beds(default)
        return default

def save_beds(beds):
    with open(BEDS_FILE, 'w') as f:
        json.dump(beds, f)

@app.route('/')
def index():
    beds = load_beds()
    icons = {
        'ICU': 'https://static.vecteezy.com/system/resources/previews/030/988/714/non_2x/hospital-bed-icon-vector.jpg',  # Friendly ICU
        'General': 'https://static.vecteezy.com/system/resources/previews/027/740/066/non_2x/sick-man-icon-in-hospital-bed-illustration-suitable-for-symbol-public-sign-emblem-web-design-free-vector.jpg',  # Welcoming general
        'Oxygen': 'https://media.istockphoto.com/id/1383930479/vector/patient-on-ventilator-life-support-on-hospital-bed.jpg?s=612x612&w=0&k=20&c=blhi94qpwb1u53RfLs-pKu09uwMsbWxX1hQ4OgC5Qa4='  # Soothing oxygen
    }
    return render_template('index.html', beds=beds, icons=icons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    beds = load_beds()
    if request.method == 'POST':
        now = str(datetime.now())
        beds['ICU']['available'] = int(request.form['icu'])
        beds['ICU']['last_updated'] = now
        beds['General']['available'] = int(request.form['general'])
        beds['General']['last_updated'] = now
        beds['Oxygen']['available'] = int(request.form['oxygen'])
        beds['Oxygen']['last_updated'] = now
        save_beds(beds)
        return redirect(url_for('admin'))
    
    return render_template('admin.html', beds=beds)

if __name__ == '__main__':
    app.run(debug=True)