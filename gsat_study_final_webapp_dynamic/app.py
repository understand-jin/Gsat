from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)

DATA_FILE = 'study_data.json'
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def init_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "혜진": {"checks": ["" for _ in range(7)], "memos": ["" for _ in range(7)]},
            "지훈": {"checks": ["" for _ in range(7)], "memos": ["" for _ in range(7)]},
            "민수": {"checks": ["" for _ in range(7)], "memos": ["" for _ in range(7)]},
            "예린": {"checks": ["" for _ in range(7)], "memos": ["" for _ in range(7)]},
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', members=data.keys())

@app.route('/member/<name>', methods=['GET', 'POST'])
def member(name):
    data = load_data()

    if request.method == 'POST':
        for i in range(7):
            data[name]['checks'][i] = '✔️' if f'day{i}' in request.form else ''
            data[name]['memos'][i] = request.form.get(f'memo{i}', '')
        save_data(data)
        return redirect(url_for('member', name=name))

    info = data[name]
    success_count = info['checks'].count('✔️')
    return render_template('member.html', name=name, checks=info['checks'],
                           memos=info['memos'], weekdays=WEEKDAYS,
                           success=success_count)

if __name__ == '__main__':
    init_data()
    app.run(debug=True)
