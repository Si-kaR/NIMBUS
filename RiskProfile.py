class RiskProfile:
    def __init__(self, risk_score=0, risk_level=""):
        self.risk_score = risk_score
        self.risk_level = risk_level

    def calculate_score(self, responses):
        # Dummy scoring algorithm based on responses
        self.risk_score = sum(responses)
        if self.risk_score < 10:
            self.risk_level = "Low"
        elif self.risk_score < 20:
            self.risk_level = "Medium"
        else:
            self.risk_level = "High"

class User:
    def __init__(self, name, age, financial_goals):
        self.name = name
        self.age = age
        self.financial_goals = financial_goals
        self.risk_profile = RiskProfile()

    def fill_out_questionnaire(self):
        # Dummy questionnaire responses
        responses = [3, 4, 2, 5]
        self.submit_responses(responses)

    def submit_responses(self, responses):
        self.risk_profile.calculate_score(responses)

class NimbusSystem:
    def analyze_responses(self, user):
        user.fill_out_questionnaire()
        return user.risk_profile

    def provide_risk_profile(self, user):
        return user.risk_profile

# Example usage
user = User("John Doe", 30, "Retirement")
nimbus_system = NimbusSystem()
nimbus_system.analyze_responses(user)
print(f"Risk Score: {user.risk_profile.risk_score}")
print(f"Risk Level: {user.risk_profile.risk_level}")
