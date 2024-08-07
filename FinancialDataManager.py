class FinancialDataManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_financial_data(self, asset_name, asset_type, current_value):
        query = """
        INSERT INTO FinancialData (AssetName, AssetType, CurrentValue)
        VALUES (%s, %s, %s)
        """
        params = (asset_name, asset_type, current_value)
        self.db.execute_query(query, params)

    # Read
    def get_financial_data(self, asset_id=None):
        if asset_id:
            query = "SELECT * FROM FinancialData WHERE AssetID = %s"
            return self.db.fetch_one(query, (asset_id,))
        else:
            query = "SELECT * FROM FinancialData"
            return self.db.fetch_all(query)

    # Update
    def update_financial_data(self, asset_id, asset_name=None, asset_type=None, current_value=None):
        query = "UPDATE FinancialData SET "
        params = []
        if asset_name:
            query += "AssetName = %s, "
            params.append(asset_name)
        if asset_type:
            query += "AssetType = %s, "
            params.append(asset_type)
        if current_value:
            query += "CurrentValue = %s, "
            params.append(current_value)
        query = query.rstrip(', ')
        query += " WHERE AssetID = %s"
        params.append(asset_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_financial_data(self, asset_id):
        query = "DELETE FROM FinancialData WHERE AssetID = %s"
        self.db.execute_query(query, (asset_id,))
