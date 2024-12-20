from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.modules.user import User
import json

def cuser_router(db):
    router = APIRouter()

    @router.post("/register")
    async def register_endpoint(user_input: User):
        collection = db["user_data"]

        # Prepare user data
        user_data = {
            "username": user_input.username,
            "password": user_input.password  
        }

        existing_user = await collection.find_one({"username": user_input.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists.")

        result = await collection.insert_one(user_data)
        if not result.acknowledged: 
            raise HTTPException(status_code=500, detail="Failed to save user to the database.")

        return Response(
            content=json.dumps({"message": "User registered successfully", "id": str(result.inserted_id)}),
            status_code=200
        )

    @router.post("/login")
    async def login_endpoint(user_input: User):
        collection = db["user_data"]

        # Find user in the database
        user = await collection.find_one({"username": user_input.username})
        if not user or user["password"] != user_input.password:
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        return Response(
            content=json.dumps({"message": "Login successful", "username": user["username"]}),
            status_code=200
        )

    return router
