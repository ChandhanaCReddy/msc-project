import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    email TEXT,
    academic_details TEXT,
    skills TEXT,
    interests TEXT,
    career_preference TEXT,
    languages TEXT,
    location TEXT,
    linkedin TEXT,
    github TEXT,
    photo TEXT,
    resume TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS reg( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,email TEXT UNIQUE , password TEXT)""")

conn.commit()
conn.close()

print("Database created")