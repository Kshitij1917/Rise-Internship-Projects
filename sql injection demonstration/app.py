from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# ✅ Toggle mode here: True = Secure, False = Vulnerable
SECURE_MODE = False

# ❌ Vulnerable version
def vulnerable_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[VULNERABLE MODE] Executing Query:", query)
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

# ✅ Secure version
def secure_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print("[SECURE MODE] Executing Query with parameters")
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def home():
    return render_template('index.html', secure_mode=SECURE_MODE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = secure_login(username, password) if SECURE_MODE else vulnerable_login(username, password)

    if user:
        return render_template('dashboard.html', user=username)
    else:
        return render_template('alert.html')

if __name__ == '__main__':
    app.run(debug=True)