class UserManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_user(self, username, risk_id):
        query = """
        INSERT INTO Users (username, risk_id)
        VALUES (%s, %s)
        """
        params = (username, risk_id)
        self.db.execute_query(query, params)

    # Register and return user_id
    def register_user(self, username, risk_id=2):
        # Check if the username already exists
        check_query = """
        SELECT user_id
        FROM users
        WHERE username = %s
        """
        check_params = (username,)
        existing_user = self.db.fetch_one(check_query, check_params)
        
        if existing_user:
            return existing_user[0]
        
        # Insert the new user
        insert_query = """
        INSERT INTO Users (username, risk_id)
        VALUES (%s, %s)
        """
        insert_params = (username, risk_id)
        self.db.execute_query(insert_query, insert_params)
        
        # Fetch the last inserted user_id
        last_id_query = "SELECT LAST_INSERT_ID() as user_id"
        result = self.db.fetch_one(last_id_query)
        return result[0]
    

    # Read
    def get_user(self, user_id=None):
        if user_id:
            query = "SELECT * FROM Users WHERE user_id = %s"
            return self.db.fetch_one(query, (user_id,))
        else:
            query = "SELECT * FROM Users"
            return self.db.fetch_all(query)

    # Get user_id by username
    def get_user_id_by_username(self, username):
        query = "SELECT user_id FROM Users WHERE username = %s"
        result = self.db.fetch_one(query, (username,))
        return result if result else None

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

    def get_risk_level(self, user_id):
        query = "SELECT risk_id FROM Users WHERE user_id = %s"
        result = self.db.fetch_one(query, (user_id,))
        return result if result else None