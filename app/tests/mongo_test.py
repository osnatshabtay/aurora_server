import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

mongo_uri = f"mongodb+srv://{username}:{password}@aurora-database.oqkwf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

db = client["aurora-database"]

user = db["user_data"].find_one({"username": "Matan"})  

print("🎯 USER FROM MONGODB:")
print(user if user else "User not found.")
