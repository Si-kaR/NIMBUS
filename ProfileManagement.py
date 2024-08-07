class ProfileManagement:
    def __init__(self):
        self.profiles = {}

    def update_personal_information(self, username, info):
        if username not in self.profiles:
            self.profiles[username] = {}
        self.profiles[username]['personal_info'] = info
        return "Personal information updated"

    def set_financial_goals(self, username, goals):
        if username not in self.profiles:
            self.profiles[username] = {}
        self.profiles[username]['financial_goals'] = goals
        return "Financial goals set"

    def update_preferences(self, username, preferences):
        if username not in self.profiles:
            self.profiles[username] = {}
        self.profiles[username]['preferences'] = preferences
        return "Preferences updated"
