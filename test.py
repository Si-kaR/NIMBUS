# Database configuration
from Database import Database

from UserManager import UserManager
from ContentGeneration import generate_content



db = Database(host="localhost", database="nimbus", user="root", password="")
db.connect()

user_manager = UserManager(db)
print(user_manager.register_user("john_doe"))

# # Example usage for InvestmentPreferencesManager
# pref_manager = InvestmentPreferencesManager(db)
# pref_manager.add_investment_preference(1, "Medium", "Conservative")

# # Example usage for FinancialDataManager
# financial_data_manager = FinancialDataManager(db)
# financial_data_manager.add_financial_data("Gold", "Commodity", 1800.00)

# # Example usage for PortfolioManager
# portfolio_manager = PortfolioManager(db)
# portfolio_manager.add_portfolio(1, "Retirement Fund")

# # Example usage for PortfolioAssetsManager
# portfolio_assets_manager = PortfolioAssetsManager(db)
# portfolio_assets_manager.add_portfolio_asset(1, 1, 50.00)



# # Example usage for UserContentProgressManager
# progress_manager = UserContentProgressManager(db)
# progress_manager.add_user_content_progress(1, 1, "InProgress")

# Disconnect from database
db.disconnect()