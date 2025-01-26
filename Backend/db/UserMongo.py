from pymongo import MongoClient

class UserMongo:
    def __init__(self, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_user(self, user_data):
        """Insert a new user into the MongoDB collection."""
        try:
            result = self.collection.insert_one(user_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error inserting user: {e}")
            return None

    def get_user_by_id(self, user_id):
        """Retrieve a user by their _id."""
        try:
            user = self.collection.find_one({"_id": user_id})
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    def update_user_contributions(self, user_id, contribution):
        """Add a contribution to the user's contributions array."""
        try:
            result = self.collection.update_one(
                {"_id": user_id},
                {"$push": {"contributions": contribution}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user contributions: {e}")
            return False

    def delete_user(self, user_id):
        """Delete a user by their _id."""
        try:
            result = self.collection.delete_one({"_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False