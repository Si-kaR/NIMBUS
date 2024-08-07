import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
