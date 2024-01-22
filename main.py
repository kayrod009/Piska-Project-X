from abc import ABC
import sqlite3
import requests

connection = sqlite3.connect("PiskaDB.db")
cursor = connection.cursor()

class Notification(ABC):
    @staticmethod
    def confirm():
        print("Done successfully")

class Appoinment:
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

class Signup:
    @staticmethod
    def sign_up(username, email, role, password):
        if role == "patient":
            globals()[f"{username}"] = Patient(username, email, password)
            # peyman = Patient("test@test", "patient", 1234)
        elif role == "staff":
            globals()[f"{username}"] = Staff(username, email, password)

class Patient(Notification, User):
    menu = "1.reserved appointments \n2.history \n3.new reservation"

    def current_reserved(self):
        self.stat_index = "11"
        # get from database
        pass
    def history(self):
        self.stat_index = "12"
        # get from database
        pass

    def new_reservation(self):
        self.stat_index = "13"
        search_key = input("search")
        # get data from database
        get_id = int(input("enter your doctor/clinic id"))
        globals()[f"{self.username}"] = Appoinment(get_id, self.id)

class Staff(Notification, User):
    menu = "1.reserved appointments \n2.cancel appointment \n3.increase capacity"

    def current_reserved(self):
        self.stat_index = "11"
        # get from database
        pass
    def cancel(self):
        appo_id = int(input("enter the appointment's id"))
        self.stat_index = "12"
        self.confirm()
        # get from database
        pass
    def increase_cap(self):
        self.stat_index = "13"
        self.confirm()
        # post to database
        pass



# class Doctor:
#     pass





class User:
    staff = dict()
    patient = dict()

    def __init__(self, username):
        self.username = username

    @staticmethod
    def sign_in(username, role):
        global status, current_user
        pass

    @staticmethod
    def make_instance(username, role):
        pass

    @staticmethod
    def sign_out():
        pass

    @staticmethod
    def back():
        pass

    @staticmethod
    def options():
        pass

    def showmenu(self):
        pass