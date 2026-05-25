from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

quotes = [
    "自律即自由",
    "今天的坚持，成就未来的你",
    "欲望越克制，人生越清醒",
    "成长来自一次次控制自己",
    "你比昨天更强"
]

# 初始化数据库
conn = sqlite3.connect('checkin.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS checkins (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('checkin.db')
    c = conn.cursor()
    c.execute('SELECT date FROM checkins ORDER BY id DESC')
    data = c.fetchall()
    conn.close()

    days = len(data)
    quote = random.choice(quotes)

    return render_template('index.html', days=days, data=data[:7], quote=quote)

@app.route('/checkin', methods=['POST'])
def checkin():
    today = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('checkin.db')
    c = conn.cursor()

    c.execute('SELECT * FROM checkins WHERE date=?', (today,))
    exist = c.fetchone()

    if not exist:
        c.execute('INSERT INTO checkins (date) VALUES (?)', (today,))
        conn.commit()

    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)