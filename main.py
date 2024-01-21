from abc import ABC

class Notification(ABC):
    @staticmethod
    def confirm():
        print("Done successfully")

