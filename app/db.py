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
