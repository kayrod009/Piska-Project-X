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