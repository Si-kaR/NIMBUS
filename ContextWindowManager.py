#table = context_window(context_id, user_id,last_response)

class ContextWindowManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_context_window(self, user_id, last_response):
        query_select = """
        SELECT * FROM ContextWindows WHERE user_id = %s
        """
        query_update = """
        UPDATE ContextWindows SET last_response = %s WHERE user_id = %s
        """
        query_insert = """
        INSERT INTO ContextWindows (user_id, last_response) VALUES (%s, %s)
        """
        
        try:
            # Execute the SELECT query
            self.db.execute_query(query_select, (user_id,))
            result = self.db.fetchone()
            
            if result:
                # If a row was returned, update the last_response
                self.db.execute_query(query_update, (last_response, user_id))
            else:
                # If no row was returned, insert a new record
                self.db.execute_query(query_insert, (user_id, last_response))
            
            # Commit the transaction
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            print(f"Error: {e}")

    # Read
    def get_context_window(self, context_window_id=None):
        if context_window_id:
            query = "SELECT * FROM ContextWindows WHERE ContextWindowID = %s"
            return self.db.fetch_one(query, (context_window_id,))
        else:
            query = "SELECT * FROM ContextWindows"
            return self.db.fetch_all(query)
        
    def get_last_response(self, user_id):
        query = "SELECT last_response FROM ContextWindows WHERE user_id = %s"
        return self.db.fetch_one(query, (user_id,))
    
    # Update
    def update_context_window(self, context_window_id, context_id=None, user_id=None, last_response=None):
        query = "UPDATE ContextWindows SET "
        params = []
        if context_id:
            query += "ContextID = %s, "
            params.append(context_id)
        if user_id:
            query += "UserID = %s, "
            params.append(user_id)
        if last_response:
            query += "LastResponse = %s, "
            params.append(last_response)
        query = query.rstrip(', ')
        query += " WHERE ContextWindowID = %s"
        params.append(context_window_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_context_window(self, context_window_id):
        query = "DELETE FROM ContextWindows WHERE ContextWindowID = %s"
        self.db.execute_query(query, (context_window_id,))