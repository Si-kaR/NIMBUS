class PortfolioManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_portfolio(self, user_id, portfolio_name):
        query = """
        INSERT INTO Portfolios (UserID, PortfolioName)
        VALUES (%s, %s)
        """
        params = (user_id, portfolio_name)
        self.db.execute_query(query, params)

    # Read
    def get_portfolio(self, portfolio_id=None):
        if portfolio_id:
            query = "SELECT * FROM Portfolios WHERE PortfolioID = %s"
            return self.db.fetch_one(query, (portfolio_id,))
        else:
            query = "SELECT * FROM Portfolios"
            return self.db.fetch_all(query)

    # Update
    def update_portfolio(self, portfolio_id, portfolio_name):
        query = "UPDATE Portfolios SET PortfolioName = %s WHERE PortfolioID = %s"
        params = (portfolio_name, portfolio_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_portfolio(self, portfolio_id):
        query = "DELETE FROM Portfolios WHERE PortfolioID = %s"
        self.db.execute_query(query, (portfolio_id,))

class PortfolioAssetsManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_portfolio_asset(self, portfolio_id, asset_id, allocation_percentage):
        query = """
        INSERT INTO PortfolioAssets (PortfolioID, AssetID, AllocationPercentage)
        VALUES (%s, %s, %s)
        """
        params = (portfolio_id, asset_id, allocation_percentage)
        self.db.execute_query(query, params)

    # Read
    def get_portfolio_assets(self, portfolio_asset_id=None):
        if portfolio_asset_id:
            query = "SELECT * FROM PortfolioAssets WHERE PortfolioAssetID = %s"
            return self.db.fetch_one(query, (portfolio_asset_id,))
        else:
            query = "SELECT * FROM PortfolioAssets"
            return self.db.fetch_all(query)

    # Update
    def update_portfolio_asset(self, portfolio_asset_id, allocation_percentage):
        query = "UPDATE PortfolioAssets SET AllocationPercentage = %s WHERE PortfolioAssetID = %s"
        params = (allocation_percentage, portfolio_asset_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_portfolio_asset(self, portfolio_asset_id):
        query = "DELETE FROM PortfolioAssets WHERE PortfolioAssetID = %s"
        self.db.execute_query(query, (portfolio_asset_id,))
