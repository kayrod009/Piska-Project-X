from abc import ABC
import pyotp
import sqlite3
import requests

connection = sqlite3.connect("PiskaDB.db")
cursor = connection.cursor()


class Notification(ABC):
    @staticmethod
    def confirm():
        print("Done successfully")

class Appoinment(Notification):
    @staticmethod
    def create(doc_id, patient_id):
        # error must be returned when getting invalid commands !
        cursor.execute("SELECT clinic_id FROM doctors WHERE doctor_id = ? ", (doc_id,))
        clinic_id = cursor.fetchone()
        insert_query = '''
                        INSERT INTO appointments (patient_id, doctor_id, clinic_id, status) VALUES (?, ?, ?, 1);
                        '''  # clinic_id
        cursor.execute(insert_query, (patient_id, doc_id, clinic_id[0]))
        cursor.execute("UPDATE clinics SET cap = cap - 1 WHERE clinic_id = ?", (clinic_id[0],))
        # sending a post request to the flask database as API
        url = 'http://localhost:5000/reserve'
        headers = {'Content-Type': 'application/json'}
        data = {'id': clinic_id[0], 'reserved': 1}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print('Reservation successful')

        connection.commit()



class User:
    staff = dict()
    patient = dict()

    def __init__(self, username):
        self.username = username

    @staticmethod
    def sign_in(username, role):
        global status, current_user
        if role == "patient":
            cursor.execute("SELECT password FROM patients WHERE username = ? ", (username,))
            usr_pas = cursor.fetchone()
        elif role == "staff":
            cursor.execute("SELECT password FROM staffs WHERE username = ? ", (username,))
            usr_pas = cursor.fetchone()
        else:
            print("your role must be staff or patient!")
            return
        if usr_pas is None:
            print("please sign up first!")
        else:
            passtype = input("password or OTP:")
            if passtype == "password":
                ask_pass = input("please enter your password: ")
                if ask_pass == usr_pas[0]:  # sign in successfully
                    User.make_instance(username, role)
                    status = "10"
                    current_user = username
                else:
                    print("Wrong password !")
            elif passtype.lower() == "otp":
                totp = pyotp.TOTP('base32secret3232')
                otp = totp.now()
                print(otp)
                ask_otp = input("please enter your OTP: ")
                if otp == ask_otp:  # sign in successfully
                    User.make_instance(username, role)
                    status = "10"
                    current_user = username
                    del otp
                else:
                    print("otp didn't match!")

    @staticmethod
    def make_instance(username, role):
        if role == "patient":
            globals()[f"{username}"] = Patient(username)
        elif role == "staff":
            globals()[f"{username}"] = Staff(username)

    @staticmethod
    def sign_out():
        global status
        status = "00"

    @staticmethod
    def back():
        global status
        if status in ["11", "12", "13"]:
            status = "10"
        elif status == "10":
            status = "00"

    @staticmethod
    def options():
        order = input("1.Back\n2.log out\n")
        if order == "Back" or order == "1":
            User.back()
        elif order == "log out" or order == "2":
            User.sign_out()

    def showmenu(self):
        print(self.menu)

class Signup:
    @staticmethod
    def sign_up(username, email, role, password):
        if role == "patient":
            globals()[f"{username}"] = Patient(username, email, password)
            # peyman = Patient("test@test", "patient", 1234)
        elif role == "staff":
            globals()[f"{username}"] = Staff(username, email, password)


class Patient(Notification, User):
    menu = "1.reserved appointments \n2.history \n3.new reservation\n4.back"

    def first_option(self):  # current reservations
        global status, cursor
        status = "11"
        cursor.execute("SELECT patient_id FROM patients WHERE username = ? ", (current_user,))
        result = cursor.fetchone()
        cursor.execute("SELECT appointment_id FROM appointments WHERE patient_id = ? AND status = 1 ", (result[0],))
        result = cursor.fetchall()
        for i in result:
            print(i[0])
        # get from database

    def second_option(self):  # show history
        global status, cursor
        # get history from database
        status = "12"
        cursor.execute("SELECT patient_id FROM patients WHERE username = ? ", (current_user,))
        result = cursor.fetchone()
        cursor.execute("SELECT appointment_id FROM appointments WHERE patient_id = ? AND status = 0 ", (result[0],))
        result = cursor.fetchall()
        for i in result:
            print(i[0])

    def third_option(self):
        global status, cursor
        cursor.execute("SELECT patient_id FROM patients WHERE username = ? ", (current_user,))
        patient_id = cursor.fetchone()
        status = "13"
        search_key = input("search: ")
        search_key = f"%{search_key}%"
        cursor.execute("SELECT clinic_id , name FROM clinics WHERE name LIKE ? AND cap != 0 ", (search_key,))
        result_1 = cursor.fetchall()
        cursor.execute('''
                       SELECT doctor_id, doctors.name
                       FROM doctors
                       JOIN clinics ON doctors.clinic_id = clinics.clinic_id
                       WHERE doctors.name LIKE ?
                       AND clinics.cap != 0
                       ''', (search_key,))
        result_2 = cursor.fetchall()
        for i in result_1:
            print(f"Clinic: {i[0]} {i[1]}")
        for i in result_2:
            print(f"Doctor: {i[0]} {i[1]}")

        # get data from database
        get_id = input("enter your doctor/clinic number(doctor/clinic number)").split()
        if get_id[0].lower() == "doctor":
            Appoinment.create(int(get_id[1]), patient_id[0])
            Appoinment.confirm()
        elif get_id[0].lower() == "clinic":
            cursor.execute('''
                                   SELECT doctor_id, doc.name
                                   FROM doctors AS doc
                                   JOIN clinics ON doc.clinic_id = clinics.clinic_id
                                   WHERE doc.clinic_id = ?
                                   ''', (int(get_id[1]),))
            result = cursor.fetchall()
            for i in result:
                print(f"Doctor: {i[0]} {i[1]}")
            doc_id = input("please choose a doctor id: ")
            Appoinment.create(doc_id, patient_id[0])
            Appoinment.confirm()

        #API handled below
        url = 'http://localhost:5000/reserve'
        headers = {'Content-Type': 'application/json'}
        data = {'id': clinic_id[0], 'reserved': 1}  # increase the reserved count
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('reservation successful')
        Appoinment.confirm()

class Staff(Notification, User):
    menu = "1.reserved appointments \n2.cancel appointment \n3.increase capacity\n4.back"

    def first_option(self):  # current reservations
        global status
        status = "11"
        cursor.execute("SELECT clinic_id FROM staffs WHERE username = ? ", (current_user,))
        clinic_id = cursor.fetchone()
        cursor.execute('''
                            SELECT appointment_id
                            FROM appointments AS app
                            JOIN clinics ON app.clinic_id = clinics.clinic_id
                            WHERE app.clinic_id = ? AND status = 1
                                 ''', (int(clinic_id[0]),))
        result = cursor.fetchall()
        for i in result:
            print(f"appointment_id: {i[0]}")

    def second_option(self):  # cancel reservations
        global status
        appo_id = int(input("enter the appointment's id: "))
        cursor.execute("SELECT clinic_id FROM appointments WHERE appointment_id = ? ", (appo_id,))
        clinic_id = cursor.fetchone()
        cursor.execute("UPDATE clinics SET cap = cap + 1 WHERE clinic_id = ?", (int(clinic_id[0]),))
        connection.commit()
        cursor.execute("UPDATE appointments SET status = status - 1 WHERE appointment_id = ?", (appo_id,))
        connection.commit()
        url = 'http://localhost:5000/reserve'
        headers = {'Content-Type': 'application/json'}
        data = {'id': clinic_id[0], 'reserved': -1}  # Decrease the reserved count
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print('Cancellation successful')
        else:
            print('Cancellation failed')
        status = "12"

        self.confirm()
        # change the appointment status on database

    def third_option(self):  # increase cap
        self.stat_index = "13"
        added_cap = int(input("how many appointments do you want to add to your clinic?: "))
        cursor.execute("SELECT clinic_id FROM staffs WHERE username = ? ", (current_user,))
        clinic_id = cursor.fetchone()
        cursor.execute("UPDATE clinics SET cap = cap + ? WHERE clinic_id = ?", (added_cap, clinic_id[0]))
        url = 'http://localhost:5000/reserve'
        headers = {'Content-Type': 'application/json'}
        data = {'id': clinic_id[0], 'reserved': -1}  # Decrease the reserved count
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print('cap increased successfully')
        else:
            print('failed to raise cap')

        connection.commit()
        self.confirm()



status = "00"
current_user = str()
print("welcome!")

while True:

    if status == "00":
        order = input("please sign up or sign in\n")
        if order.lower() in ["sign up", "signup"]:
            info = {
                "username": "",
                "email": "",
                "role(patient/staff)": "",
                "password": ""
            }
            for item in info:
                info[f"{item}"] = input(f"please enter your {item}: ")
            Signup.sign_up(info["username"], info["email"], info["role(patient/staff)"], info["password"])
        elif order.lower() in ["sign in", "signin"]:
            username = input("please enter your username: ")
            role = input("please enter your role: ")
            User.sign_in(username, role)

    elif status == "10":
        pass
        if order == "1":
            pass
        elif order == "2":
            pass
        elif order == "3":
            pass
        elif order == "4":
            pass

    elif status in ["11", "12", "13"]:
        pass