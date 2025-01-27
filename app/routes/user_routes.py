from app.services.users.password_validator import password_validator
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.modules.user import User
from app.db import get_db_conn
import json
from app.services.users.session import set_current_user, get_current_user
from pymongo import ASCENDING

current_user = None

router = APIRouter()

@router.post("/register")
async def register_endpoint(user_input: User, db_conn=Depends(get_db_conn)):
    collection = db_conn["user_data"]
    
    password_error = password_validator(user_input.password)
    if password_error:
        raise HTTPException(status_code=400, detail=password_error)

    # Ensure the user provides agreement to the regulations
    if not user_input.agreement:
        raise HTTPException(status_code=400, detail="User agreement is required to register.")


    # Prepare user data
    user_data = {
        "username": user_input.username,
        "password": user_input.password,
        "agreement": user_input.agreement,  
    }

    existing_user = await collection.find_one({"username": user_input.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    result = await collection.insert_one(user_data)
    if not result.acknowledged: 
        raise HTTPException(status_code=500, detail="Failed to save user to the database.")
    
    set_current_user(user_input)

    return Response(
        content=json.dumps({"message": "User registered successfully", "id": str(result.inserted_id)}),
        status_code=200
    )

@router.post("/login")
async def login_endpoint(user_input: User, db_conn=Depends(get_db_conn)):
    collection = db_conn["user_data"]

    user = await collection.find_one({"username": user_input.username})
    if not user or user["password"] != user_input.password:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    set_current_user(user) 

    return Response(
        content=json.dumps({"message": "Login successful", "username": user["username"]}),
        status_code=200
    )


@router.get("/questions")
async def questions_endpoint(db_conn=Depends(get_db_conn)):

    collection = db_conn["questions"]
    questions_cursor = collection.find().sort("index", ASCENDING)
    questions = await questions_cursor.to_list(length=None)  
    
    for question in questions:
        if "_id" in question:
            question["_id"] = str(question["_id"])

    return {"questions": questions}

@router.post("/questions")
async def questions_endpoint(answers: dict, db_conn=Depends(get_db_conn)):

    current_user = get_current_user()

    if not current_user:
        raise HTTPException(status_code=401, detail="User is not authenticated")

    collection = db_conn["user_data"]

    # Extract gender and image URL from the incoming payload
    gender = answers.get("gender")
    selected_image = answers.get("selectedImage")

    try:
        # Update the user's answers, gender, and selected image URL
        collection.update_one(
            {'username': current_user.username}, 
            {
                "$set": {
                    "answers": answers.get("answers"),  
                    "gender": gender,                 
                    "selectedImage": selected_image    
                }
            }
        )

        if gender:
            current_user.gender = gender
        if selected_image:
            current_user.selectedImage = selected_image
            
        return Response(
            content=json.dumps({"message": "Answers, gender, and image URL saved successfully"}),
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


