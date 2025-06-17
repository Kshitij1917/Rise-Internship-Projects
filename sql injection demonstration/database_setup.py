import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Add test user: admin / admin123
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
conn.commit()
conn.close()
print("Database setup complete.")