import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@aurora-database.oqkwf.mongodb.net/"
    "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
)
DATABASE_NAME = "aurora-database"

# # MongoDB class for connection management
# class MongoDB:
#     def __init__(self, uri: str, db_name: str):
#         self.uri = uri
#         self.db_name = db_name
#         self.client = None

#     async def __aenter__(self):
#         if not self.client:
#             self.client = AsyncIOMotorClient(self.uri)
#         return self.client[self.db_name]

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         pass
#         # if self.client:
#         #     self.client.close()

# # MongoDB instance
# mongo_instance = MongoDB(uri=MONGO_URL, db_name=DATABASE_NAME)

# # Dependency for database access
# async def get_db_conn():
#     async with mongo_instance as db:
#         yield db


mongo_client = None

async def init_mongo_client():
    global mongo_client
    if not mongo_client:
        mongo_client = AsyncIOMotorClient(MONGO_URL)

async def get_database():
    if not mongo_client:
        await init_mongo_client()
    return mongo_client[DATABASE_NAME]

async def get_db_conn():
    db = await get_database()
    yield db

async def close_mongo_client():
    global mongo_client
    if mongo_client:
        mongo_client.close()
