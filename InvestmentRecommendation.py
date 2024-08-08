class recommended_investments:
    def __init__(self, db):
        self.db = db

    # Create
    def add_recommendation(self, user_id, description, risk_level):
        query = """
        INSERT INTO recommended_investments (user_id, Description, risk_level)
        VALUES (%s, %s, %s)
        """
        params = (user_id, description, risk_level)
        self.db.execute_query(query, params)

    # Read
    def get_recommendation(self, recommendation_id=None):
        if recommendation_id:
            query = "SELECT * FROM recommended_investments WHERE rec_id = %s"
            return self.db.fetch_one(query, (recommendation_id,))
        else:
            query = "SELECT * FROM recommended_investments"
            return self.db.fetch_all(query)
        
    # Update
    def update_recommendation(self, recommendation_id, user_id=None, description=None, risk_level=None):
        query = "UPDATE recommended_investments SET "
        params = []
        if user_id:
            query += "user_id = %s, "
            params.append(user_id)
        if description:
            query += "Description = %s, "
            params.append(description)
        if risk_level:
            query += "risk_level = %s, "
            params.append(risk_level)
        query = query.rstrip(', ')
        query += " WHERE rec_id = %s"
        params.append(recommendation_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_recommendation(self, recommendation_id):
        query = "DELETE FROM recommended_investments WHERE rec_id = %s"
        self.db.execute_query(query, (recommendation_id,))

    # Read by User
    def get_recommendation_by_user(self, user_id):
        query = "SELECT * FROM recommended_investments WHERE user_id = %s"
        return self.db.fetch_all(query, (user_id,))
    
    # Read by Risk Level
    def get_recommendation_by_risk_level(self, risk_level):
        query = "SELECT * FROM recommended_investments WHERE risk_level = %s"
        return self.db.fetch_all(query, (risk_level,))
    
    # Delete by User
    def delete_recommendation_by_user(self, user_id):
        query = "DELETE FROM recommended_investments WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))
