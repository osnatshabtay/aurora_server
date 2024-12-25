from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

from app.routes.user_routes import cuser_router

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@aurora-database.oqkwf.mongodb.net/"
    "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
)
DATABASE_NAME = "aurora-database"


app = FastAPI()

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

app.include_router(cuser_router(db), prefix="/users", tags=["Users"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
