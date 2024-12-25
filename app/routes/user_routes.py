from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.modules.user import User
import json

current_user = None

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
        
        global current_user
        current_user = user_input 

        return Response(
            content=json.dumps({"message": "User registered successfully", "id": str(result.inserted_id)}),
            status_code=200
        )

    @router.post("/login")
    async def login_endpoint(user_input: User):
        collection = db["user_data"]

        user = await collection.find_one({"username": user_input.username})
        if not user or user["password"] != user_input.password:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        
        global current_user
        current_user = user_input 

        return Response(
            content=json.dumps({"message": "Login successful", "username": user["username"]}),
            status_code=200
        )
    
    @router.get("/questions")
    async def questions_endpoint():
        collection = db["questions"]
        questions_cursor = collection.find()
        questions = await questions_cursor.to_list(length=None)  
        
        for question in questions:
            if "_id" in question:
                question["_id"] = str(question["_id"])

        return {"questions": questions}
    
    @router.post("/questions")
    async def questions_endpoint(answers : dict):

        global current_user

        if not current_user:
            raise HTTPException(status_code=401, detail="User is not authenticated")

        collection = db["user_data"]

        try:
            collection.update_one(
                {'username': current_user.username}, 
                {
                    "$set": {
                        "answers": answers 
                    }
                }
            )
            return Response(
                    content=json.dumps({"message": "Answers saved successfully"}),
                    status_code=200
                )        
        
        except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")




    return router
