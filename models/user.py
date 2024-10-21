from db import create_connection

class UserModel:
    def __init__(self, _id, username ,password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            return cls(*row)
    
    @classmethod
    def find_by_id(cls, id):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            return cls(*row)

    def save_to_db(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(query, (self.username, self.password,))
        conn.commit()
        conn.close()