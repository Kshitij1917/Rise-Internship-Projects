# SQL Injection Demonstration

## ❓ What is SQL Injection?
SQL Injection is a vulnerability where attackers manipulate SQL queries by injecting malicious input, often through form fields.

## 🔓 Vulnerable Scenario
Enter:
```
username: ' OR '1'='1
password: anything
```
This bypasses login due to unsanitized input.

## 🔒 Secure Fix
Use parameterized queries to separate code from user input:
```python
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
```

## 🛡 Best Practices
- Always validate and sanitize input
- Use ORM or parameterized queries
- Avoid showing detailed DB errors

## 🚀 To Run
```bash
pip install flask
python database_setup.py
python app.py
```
Then open: http://127.0.0.1:5000