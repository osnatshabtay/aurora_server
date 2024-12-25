from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os

from app.routes.user_routes import router

app = FastAPI()

app.include_router(router, prefix="/users", tags=["Users"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
