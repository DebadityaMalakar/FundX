import io
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.User import User
from db.UserMongo import UserMongo
from db.Business import Business
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
import hashlib
import sqlite3
import base64

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize databases
user_db = User("base.db")  # SQLite User database
user_mongo = UserMongo("test_db", "users")  # MongoDB User database
business_db = Business("base.db")  # SQLite Business database

# Helper functions
def generate_salt():
    """Generate a salt using the current datetime."""
    return hashlib.sha256(str(datetime.now()).encode()).hexdigest()

def hash_data(data, salt):
    """Hash data using SHA-256 and a salt."""
    return hashlib.sha256((data + salt).encode()).hexdigest()

# Pydantic models for request validation
class SignupRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str
    acc_type: str = "user"  # Default to "user" if not provided

class LoginRequest(BaseModel):
    username: str
    password: str

# Routes
@app.post("/api/signup")
def signup(user: SignupRequest):
    """
    Signup a new user.
    """
    # Generate salt and hash password
    salt = generate_salt()
    hashed_password = hash_data(user.password, salt)

    # Generate _id using hash(username + salt)
    _id = hash_data(user.username, salt)

    # Insert into SQLite
    user_data = (
        _id,
        user.name,
        user.username,
        user.email,
        hashed_password,
        salt,
        user.acc_type,  # Use the provided acc_type or default to "user"
    )
    user_id = user_db.insert_user(user_data)
    if not user_id:
        raise HTTPException(status_code=400, detail="Failed to create user in SQLite.")

    # Insert into MongoDB
    mongo_data = {"_id": _id, "contributions": []}
    mongo_id = user_mongo.insert_user(mongo_data)
    if not mongo_id:
        raise HTTPException(status_code=400, detail="Failed to create user in MongoDB.")

    return {"message": "User created successfully", "user_id": user_id, "mongo_id": mongo_id}

@app.post("/api/login")
def login(credentials: LoginRequest):
    """
    Login a user.
    """
    # Fetch user from SQLite
    user = user_db.get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Verify password
    salt = user[6]  # Salt is at index 6
    hashed_password = hash_data(credentials.password, salt)
    if user[5] != hashed_password:  # Hashed password is at index 5
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {"message": "Login successful", "user": user}

@app.delete("/api/delete")
def delete_account(account: str = Query(..., description="The _id of the user to delete")):
    """
    Delete a user account.
    """
    # Delete from SQLite
    user = user_db.get_user_by_username(account)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in SQLite.")

    deleted = user_db.delete_user(user[0])  # user[0] is the SQLite ID
    if not deleted:
        raise HTTPException(status_code=400, detail="Failed to delete user from SQLite.")

    # Delete from MongoDB
    deleted_mongo = user_mongo.delete_user(account)
    if not deleted_mongo:
        raise HTTPException(status_code=400, detail="Failed to delete user from MongoDB.")

    return {"message": "User deleted successfully"}

@app.get("/api/businesses")
def get_all_businesses():
    """
    Retrieve all businesses from the database and return as JSON.
    """
    query = "SELECT * FROM Business;"
    try:
        with sqlite3.connect(business_db.db_path) as conn:  # Use the same SQLite path as initialized
            cursor = conn.cursor()
            cursor.execute(query)
            businesses = cursor.fetchall()

        # Format the result into a list of dictionaries
        business_list = [
            {
                "name": business[0],
                "description": business[1],
                "owner": business[2],
                "owner_mail": business[3],
                "owner_phone": business[4],
                "img_blob": f"/api/image/{hashlib.sha256(business[0].encode()).hexdigest()}",
                "img_type": business[6],
                "upi_id": business[7]
            }
            for business in businesses
        ]
        return {"businesses": business_list}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving businesses: {e}")

@app.get("/api/image/{shash}")
def get_image(shash: str):
    """
    Retrieve the image for a business using the hash of the business name.
    """
    query = "SELECT name, img_blob, img_type FROM Business;"
    
    try:
        with sqlite3.connect(business_db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            businesses = cursor.fetchall()

        # Iterate through businesses to match the hash
        for name, img_blob, img_type in businesses:
            generated_hash = hashlib.sha256(name.encode()).hexdigest()
            if generated_hash == shash:
                if img_blob:
                    # Convert the binary data into a bytes-like object and return it as a streaming response
                    return StreamingResponse(io.BytesIO(img_blob), media_type=img_type)
                else:
                    raise HTTPException(status_code=404, detail="Image not found.")
        
        # If no match is found
        raise HTTPException(status_code=404, detail="Business with given hash not found.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {e}")
    
@app.get("/api/business/{name}")
def get_business_by_name(name: str):
    """
    Retrieve a specific business by its name.
    """
    try:
        # Fetch the business from the database
        business = business_db.get_business_by_name(name)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        # Generate the image hash URL if img_blob is present
        img_url = None
        if business[5]:  # img_blob is at index 5
            img_url = f"/api/image/{hashlib.sha256(name.encode()).hexdigest()}"

        # Return business details as a JSON response
        return {
            "name": business[0],
            "description": business[1],
            "owner": business[2],
            "owner_mail": business[3],
            "owner_phone": business[4],
            "img_blob": img_url,
            "img_type": business[6],
            "upi_id": business[7],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
