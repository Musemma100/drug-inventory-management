class User:
    def __init__(self, username):
        self.username = username

    def get_role(self):
        return "User"

class Pharmacist(User):
    def get_role(self):
        return "Pharmacist"
