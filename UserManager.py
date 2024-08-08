class UserManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_user(self, user_id, username, risk_id):
        query = """
        INSERT INTO Users (user_id, username, risk_id)
        VALUES (%s, %s, %s)
        """
        params = (user_id, username, risk_id)
        self.db.execute_query(query, params)

    # Read
    def get_user(self, user_id=None):
        if user_id:
            query = "SELECT * FROM Users WHERE user_id = %s"
            return self.db.fetch_one(query, (user_id,))
        else:
            query = "SELECT * FROM Users"
            return self.db.fetch_all(query)

    # Update
    def update_user(self, user_id, username=None, risk_id=None):
        query = "UPDATE Users SET "
        params = []
        if username:
            query += "username = %s, "
            params.append(username)
        if risk_id:
            query += "risk_id = %s, "
            params.append(risk_id)
        query = query.rstrip(', ')
        query += " WHERE user_id = %s"
        params.append(user_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))

    