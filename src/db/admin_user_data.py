
class AdminUserData():
    def __init__(self, name, email, password_hash, role):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role