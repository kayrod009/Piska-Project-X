from abc import ABC
import pyotp

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