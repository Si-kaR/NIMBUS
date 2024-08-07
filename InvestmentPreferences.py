class InvestmentPreferencesManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_investment_preference(self, user_id, risk_tolerance='Medium', diversification_level='Balanced'):
        query = """
        INSERT INTO InvestmentPreferences (UserID, RiskTolerance, DiversificationLevel)
        VALUES (%s, %s, %s)
        """
        params = (user_id, risk_tolerance, diversification_level)
        self.db.execute_query(query, params)

    # Read
    def get_investment_preferences(self, preference_id=None):
        if preference_id:
            query = "SELECT * FROM InvestmentPreferences WHERE PreferenceID = %s"
            return self.db.fetch_one(query, (preference_id,))
        else:
            query = "SELECT * FROM InvestmentPreferences"
            return self.db.fetch_all(query)

    # Update
    def update_investment_preference(self, preference_id, risk_tolerance=None, diversification_level=None):
        query = "UPDATE InvestmentPreferences SET "
        params = []
        if risk_tolerance:
            query += "RiskTolerance = %s, "
            params.append(risk_tolerance)
        if diversification_level:
            query += "DiversificationLevel = %s, "
            params.append(diversification_level)
        query = query.rstrip(', ')
        query += " WHERE PreferenceID = %s"
        params.append(preference_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_investment_preference(self, preference_id):
        query = "DELETE FROM InvestmentPreferences WHERE PreferenceID = %s"
        self.db.execute_query(query, (preference_id,))
