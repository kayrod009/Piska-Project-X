from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

@app.route('/slots', methods=['GET'])
def get_slots():
    connection = sqlite3.connect('PiskaDB.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clinics")
    clinics = cursor.fetchall()
    connection.close()
    return jsonify({clinic[0]: clinic[2] for clinic in clinics})

@app.route('/reserve', methods=['POST'])
def reserve_slot():
    data = request.json
    clinic_id = data.get('id')
    reserved = data.get('reserved', 0)

    connection = sqlite3.connect('PiskaDB.db')
    cursor = connection.cursor()

    cursor.execute("SELECT cap FROM clinics WHERE clinic_id = ?", (clinic_id,))
    current_capacity = cursor.fetchone()[0]

    if current_capacity and current_capacity >= reserved:
        cursor.execute("UPDATE clinics SET cap = cap - ? WHERE clinic_id = ?", (reserved, clinic_id))
        connection.commit()

        cursor.execute("SELECT cap FROM clinics WHERE clinic_id = ?", (clinic_id,))
        new_capacity = cursor.fetchone()[0]

        connection.close()
        return jsonify({"success": True, "remaining_slots": new_capacity})
    else:
        connection.close()
        return jsonify({"success": False, "message": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)

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

# In-memory database from our Flask code
database = {
    "1": 25,
    "2": 15,
    "3": 15,
    "4": 20,
    "5": 30,
    "6": 9,
    "7": 8
}

# Insert the clinics into the clinics table
for clinic_id, cap in database.items():
    name = f'clinic {clinic_id}'
    cursor.execute('''
    INSERT INTO clinics (clinic_id, name, cap) VALUES (?, ?, ?)
    ''', (clinic_id, name, cap))
connection.commit()


connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);
''')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clinics (
    clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cap INTEGER NOT NULL
);
''')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clinics (
    clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cap INTEGER NOT NULL
);
''')
connection.commit()
connection.close()