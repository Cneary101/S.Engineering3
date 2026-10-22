class Login():

    def __init__(self, username, password):
        self.username = username
        self.password = password
    #Username must be between 6 and 12 characters inclusive
    def verifyUsername(self):
        if not isinstance(self.username, str):
            return False
        return 6 <= len(self.username) <= 12

    #Password must contain 4 to 6 digits inclusive
    def verifyPassword(self):
        if not isinstance(self.password, str):
            return False
        if not self.password.isdigit():
            return False
        return 4 <= len(self.password) <= 6
    #Verifies that both the username and the login are valid
    def verifyLogin(self):
        return self.verifyUsername() and self.verifyPassword()