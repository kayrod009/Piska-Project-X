from abc import ABC

class Notification(ABC):
    @staticmethod
    def confirm():
        print("Done successfully")

class Signup:

    def __init__(self, username, email, role, password):

        if role == "patient":
            globals()[f"{username}"] = Patient(username, email, password)
            # peyman = Patient("test@test", "patient", 1234)
        elif role == "staff":
            globals()[f"{username}"] = Staff(username, email, password)


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