import sqlite3

connection = sqlite3.connect('PiskaDB.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
''')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS staffs (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
''')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    clinic_id INTEGER,
    FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
);
''')

connection.commit()