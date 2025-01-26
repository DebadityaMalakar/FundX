import sqlite3
from sqlite3 import Error

class User:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()
        #self.create_anonymous_user()  # Ensure the anonymous user exists

    def create_table(self):
        """Create the User table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            _id TEXT NOT NULL,
            Name TEXT NOT NULL,
            Username TEXT NOT NULL UNIQUE,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Salt TEXT NOT NULL,
            AccType TEXT NOT NULL
        );
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
        except Error as e:
            print(f"Error creating User table: {e}")

    # def create_anonymous_user(self):
    #     """Create a default anonymous user if it doesn't exist."""
    #     anonymous_user = (
    #         "anonymous_id",  # _id
    #         "Anonymous User",  # Name
    #         "anonymous",  # Username
    #         "anonymous@example.com",  # Email
    #         "anonymous_password",  # Password
    #         "anonymous_salt",  # Salt
    #         "anonymous"  # AccType
    #     )

    #     # Check if the anonymous user already exists
    #     existing_user = self.get_user_by_username("anonymous")
    #     if existing_user is None:
    #         # Insert the anonymous user
    #         self.insert_user(anonymous_user)
    #         print("Anonymous user created successfully.")
    #     else:
    #         print("Anonymous user already exists.")

    def insert_user(self, user_data):
        """Insert a new user into the User table."""
        query = """
        INSERT INTO User (_id, Name, Username, Email, Password, Salt, AccType)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, user_data)
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Error inserting user: {e}")
            return None

    def get_user_by_username(self, username):
        """Retrieve a user by their username."""
        query = "SELECT * FROM User WHERE Username = ?;"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (username,))
                return cursor.fetchone()
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        query = "SELECT * FROM User WHERE Email = ?;"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None

    def update_user(self, user_id, updated_data):
        """Update a user's information."""
        query = """
        UPDATE User
        SET Name = ?, Username = ?, Email = ?, Password = ?, Salt = ?, AccType = ?
        WHERE id = ?;
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (*updated_data, user_id))
                conn.commit()
                return True
        except Error as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id):
        """Delete a user by their ID."""
        query = "DELETE FROM User WHERE id = ?;"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user_id,))
                conn.commit()
                return True
        except Error as e:
            print(f"Error deleting user: {e}")
            return False