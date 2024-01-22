from abc import ABC
import pyotp
import sqlite3

connection = sqlite3.connect("PiskaDB.db")
cursor = connection.cursor()


class Notification(ABC):
    @staticmethod
    def confirm():
        print("Done successfully")


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


class Appoinment:
    pass


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
        order = input("1.Back\n2.Fuck off\n")
        if order == "Back" or order == "1":
            User.back()
        elif order == "Fuck off" or order == "2":
            User.sign_out()

    def showmenu(self):
        print(self.menu)
