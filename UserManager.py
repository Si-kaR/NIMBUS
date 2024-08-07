class UserManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_user(self, username, password_hash, email, risk_tolerance='Medium'):
        query = """
        INSERT INTO Users (Username, PasswordHash, Email, RiskTolerance)
        VALUES (%s, %s, %s, %s)
        """
        params = (username, password_hash, email, risk_tolerance)
        self.db.execute_query(query, params)

    # Read
    def get_user(self, user_id=None):
        if user_id:
            query = "SELECT * FROM Users WHERE UserID = %s"
            return self.db.fetch_one(query, (user_id,))
        else:
            query = "SELECT * FROM Users"
            return self.db.fetch_all(query)

    # Update
    def update_user(self, user_id, username=None, password_hash=None, email=None, risk_tolerance=None):
        query = "UPDATE Users SET "
        params = []
        if username:
            query += "Username = %s, "
            params.append(username)
        if password_hash:
            query += "PasswordHash = %s, "
            params.append(password_hash)
        if email:
            query += "Email = %s, "
            params.append(email)
        if risk_tolerance:
            query += "RiskTolerance = %s, "
            params.append(risk_tolerance)
        query = query.rstrip(', ')
        query += " WHERE UserID = %s"
        params.append(user_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE UserID = %s"
        self.db.execute_query(query, (user_id,))
