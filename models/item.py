from db import create_connection

class ItemModel:
    def __init__(self, _id, name ,price, owner_id):
        self.id = _id
        self.name = name
        self.price = price
        self.owner_id = owner_id
    
    @classmethod
    def find_by_username(cls, name):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            return cls(*row)
    
    @classmethod
    def find_by_id(cls, id):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            return cls(*row)

    @classmethod
    def find_all(cls, name):
        conn = create_connection()
        cursor = conn.cursor()
        
        if name:
            query = "SELECT * FROM items WHERE name LIKE ?"
            # Include the '%' wildcard in the parameter value
            result = cursor.execute(query, (f"%{name}%",))
        else:
            query = "SELECT * FROM items"
            result = cursor.execute(query)
        
        rows = result.fetchall()
        return [cls(*row) for row in rows]

    def save_to_db(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO items (name, price, owner_id) VALUES (?, ?, ?)"
        cursor.execute(query, (self.name, self.price, self.owner_id,))
        conn.commit()
        conn.close()
