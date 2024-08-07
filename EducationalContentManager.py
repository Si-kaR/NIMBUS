class EducationalContentManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_educational_content(self, title, content_type, content, topic, risk):
        query = """
        INSERT INTO EducationalContent (Title, ContentType, Content, Topic, risk_type, CreatedAt)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        params = (title, content_type, content, topic, risk)
        self.db.execute_query(query, params)

    # Read
    def get_educational_content(self, content_id=None):
        if content_id:
            query = "SELECT * FROM EducationalContent WHERE ContentID = %s"
            return self.db.fetch_one(query, (content_id,))
        else:
            query = "SELECT * FROM EducationalContent"
            return self.db.fetch_all(query)

    # Update
    def update_educational_content(self, content_id, title=None, content_type=None, content=None, topic=None):
        query = "UPDATE EducationalContent SET "
        params = []
        if title:
            query += "Title = %s, "
            params.append(title)
        if content_type:
            query += "ContentType = %s, "
            params.append(content_type)
        if content:
            query += "Content = %s, "
            params.append(content)
        if topic:
            query += "Topic = %s, "
            params.append(topic)
        query = query.rstrip(', ')
        query += " WHERE ContentID = %s"
        params.append(content_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_educational_content(self, content_id):
        query = "DELETE FROM EducationalContent WHERE ContentID = %s"
        self.db.execute_query(query, (content_id,))

class UserContentProgressManager:
    def __init__(self, db):
        self.db = db

    # Create
    def add_user_content_progress(self, user_id, content_id, progress='NotStarted'):
        query = """
        INSERT INTO UserContentProgress (UserID, ContentID, Progress)
        VALUES (%s, %s, %s)
        """
        params = (user_id, content_id, progress)
        self.db.execute_query(query, params)

    # Read
    def get_user_content_progress(self, progress_id=None):
        if progress_id:
            query = "SELECT * FROM UserContentProgress WHERE ProgressID = %s"
            return self.db.fetch_one(query, (progress_id,))
        else:
            query = "SELECT * FROM UserContentProgress"
            return self.db.fetch_all(query)

    # Update
    def update_user_content_progress(self, progress_id, progress=None, last_accessed=None):
        query = "UPDATE UserContentProgress SET "
        params = []
        if progress:
            query += "Progress = %s, "
            params.append(progress)
        if last_accessed:
            query += "LastAccessed = %s, "
            params.append(last_accessed)
        query = query.rstrip(', ')
        query += " WHERE ProgressID = %s"
        params.append(progress_id)
        self.db.execute_query(query, params)

    # Delete
    def delete_user_content_progress(self, progress_id):
        query = "DELETE FROM UserContentProgress WHERE ProgressID = %s"
        self.db.execute_query(query, (progress_id,))
