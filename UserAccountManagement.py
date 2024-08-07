import hashlib

class UserAccountManagement:
    def __init__(self):
        self.users = {}
        self.logged_in_users = {}

    def register(self, username, password):
        if username in self.users:
            return "Username already exists"
        self.users[username] = hashlib.sha256(password.encode()).hexdigest()
        return "User registered successfully"

    def log_in(self, username, password):
        if username in self.users and self.users[username] == hashlib.sha256(password.encode()).hexdigest():
            self.logged_in_users[username] = True
            return "User logged in successfully"
        return "Invalid username or password"

    def log_out(self, username):
        if username in self.logged_in_users:
            del self.logged_in_users[username]
            return "User logged out successfully"
        return "User not logged in"

    def change_password(self, username, old_password, new_password):
        if username in self.users and self.users[username] == hashlib.sha256(old_password.encode()).hexdigest():
            self.users[username] = hashlib.sha256(new_password.encode()).hexdigest()
            return "Password changed successfully"
        return "Invalid username or password"

    def enable_two_factor_authentication(self, username):
        # Placeholder for actual two-factor authentication implementation
        return "Two-factor authentication enabled"

    def review_account_activity(self, username):
        # Placeholder for actual account activity review implementation
        return "Account activity reviewed"
