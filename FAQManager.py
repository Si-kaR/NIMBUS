class FAQManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_faq(self, question):
        query_select = """
        SELECT * FROM frequent_terms WHERE search_term = %s
        """
        query_update = """
        UPDATE frequent_terms SET frequency = frequency + 1 WHERE search_term = %s
        """
        query_insert = """
        INSERT INTO frequent_terms (search_term, frequency) VALUES (%s, 1)
        """
        
        try:
            # Execute the SELECT query
            result = self.db.fetch_one(query_select, (question,))
            
            if result:
                # If a row was returned, update the frequency by 1
                self.db.execute_query(query_update, (question,))
            else:
                # If no row was returned, insert a new record with frequency set to 1
                self.db.execute_query(query_insert, (question,))
            
        except Exception as e:
            print(f"Error: {e}")

    # Read
    def get_faq(self, number_of_results=10):
        query = """
        SELECT search_term FROM frequent_terms ORDER BY frequency DESC LIMIT %s
        """
        try:
            result = self.db.fetch_all(query, (number_of_results,))
            for i in range(len(result)):
                result[i] = result[i][0]
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    # Delete
    def delete_faq(self, question):
        query = """
        DELETE FROM frequent_terms WHERE search_term = %s
        """
        try:
            self.db.execute_query(query, (question,))
        except Exception as e:
            print(f"Error: {e}")

    # Update
    def update_faq(self, old_question, new_question):
        query = """
        UPDATE frequent_terms SET search_term = %s WHERE search_term = %s
        """
        try:
            self.db.execute_query(query, (new_question, old_question))
        except Exception as e:
            print(f"Error: {e}")

    # Read All
    def get_all_faq(self):
        query = """
        SELECT * FROM frequent_terms
        """
        try:
            result = self.db.fetch_all(query)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

# db = Database.Database(host='localhost', database = 'nimbus', user = 'root', password = '')
# db.connect()
# test = FAQManager(db)

# print(test.get_faq())