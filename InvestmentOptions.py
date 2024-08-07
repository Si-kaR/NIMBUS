class InvestmentOptions:
    def __init__(self):
        self.options = []

    def generate_options(self, risk_profile):
        # Dummy investment options based on risk profile
        if risk_profile.risk_level == "Low":
            self.options = ["Bonds", "Savings Account"]
        elif risk_profile.risk_level == "Medium":
            self.options = ["Index Funds", "Mutual Funds"]
        else:
            self.options = ["Stocks", "Cryptocurrency"]

class InvestmentPortfolio:
    def __init__(self):
        self.assets = []

    def diversify(self, investment_options):
        # Dummy diversification logic
        self.assets = investment_options.options

class NimbusSystem:
    def generate_investment_options(self, risk_profile):
        investment_options = InvestmentOptions()
        investment_options.generate_options(risk_profile)
        return investment_options

    def create_diversified_portfolio(self, investment_options):
        portfolio = InvestmentPortfolio()
        portfolio.diversify(investment_options)
        return portfolio

    def provide_investment_suggestions(self, portfolio):
        return portfolio.assets

# Example usage
risk_profile = RiskProfile(15, "Medium")
nimbus_system = NimbusSystem()
investment_options = nimbus_system.generate_investment_options(risk_profile)
portfolio = nimbus_system.create_diversified_portfolio(investment_options)
suggestions = nimbus_system.provide_investment_suggestions(portfolio)
print(f"Investment Suggestions: {suggestions}")
