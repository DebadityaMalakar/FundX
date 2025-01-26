import sqlite3
from sqlite3 import Error

class Business:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Create the Business table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS Business (
            name TEXT NOT NULL,
            description TEXT,
            owner TEXT NOT NULL,
            owner_mail TEXT NOT NULL,
            owner_phone TEXT NOT NULL,
            img_blob BLOB,
            img_type TEXT,
            upi_id TEXT
        );
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
        except Error as e:
            print(f"Error creating Business table: {e}")

    def insert_business(self, business_data):
        """Insert a new business into the Business table."""
        query = """
        INSERT INTO Business (name, description, owner, owner_mail, owner_phone, img_blob, img_type,upi_id)
        VALUES (?, ?, ?, ?, ?, ?, ?,?);
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, business_data)
                conn.commit()
                return True
        except Error as e:
            print(f"Error inserting business: {e}")
            return False

    def get_business_by_name(self, name):
        """Retrieve a business by its name."""
        query = "SELECT * FROM Business WHERE name = ?;"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (name,))
                return cursor.fetchone()
        except Error as e:
            print(f"Error retrieving business: {e}")
            return None

    def update_business(self, name, updated_data):
        """Update a business's information."""
        query = """
        UPDATE Business
        SET description = ?, owner = ?, owner_mail = ?, owner_phone = ?, img_blob = ?, img_type = ?
        WHERE name = ?;
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (*updated_data, name))
                conn.commit()
                return True
        except Error as e:
            print(f"Error updating business: {e}")
            return False

    def delete_business(self, name):
        """Delete a business by its name."""
        query = "DELETE FROM Business WHERE name = ?;"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (name,))
                conn.commit()
                return True
        except Error as e:
            print(f"Error deleting business: {e}")
            return False