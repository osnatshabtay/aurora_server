from app.services.recommendations.classify_user_recom import classify_user_profile_from_db
from app.services.users.password_validator import password_validator
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.modules.user import User
from app.db import get_db_conn
import json
from pymongo import ASCENDING
from app.services.users.auth import create_access_token, get_current_user
from app.models.social_graph import process_questionnaire_answers

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

    # Block reserved usernames
    if user_input.username.strip().lower() == "admin":
        raise HTTPException(status_code=400, detail="Cannot register with reserved username 'admin'.")

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
    
    access_token = create_access_token(data={"sub": user_input.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(result.inserted_id),
    }

@router.post("/login")
async def login_endpoint(user_input: User, db_conn=Depends(get_db_conn)):
    print(f"📥 Received login for user: {user_input.username}")
    collection = db_conn["user_data"]
    user = await collection.find_one({"username": user_input.username})

    if not user or user["password"] != user_input.password:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    access_token = create_access_token(data={"sub": user["username"]})
    is_admin = user["username"] == "Admin"

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_admin": is_admin
    }
    set_current_user(User(**user)) 

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
async def questions_endpoint(
    answers: dict, 
    current_user=Depends(get_current_user), 
    db_conn=Depends(get_db_conn)
):
    collection = db_conn["user_data"]

    gender = answers.get("gender")
    selected_image = answers.get("selectedImage")
    classified_profile = classify_user_profile_from_db(answers.get("answers"))

    try:
        await collection.update_one(
            {'username': current_user["username"]}, 
            {
                "$set": {
                    "answers": answers.get("answers"),
                    "gender": gender,
                    "selectedImage": selected_image,
                    "classified_profile": classified_profile
                }
            }
        )
    
        if gender:
             current_user["gender"] = gender
        if selected_image:
            current_user["selectedImage"] = selected_image
            
        # Process the questionnaire answers to generate recommendations
        await process_questionnaire_answers(answers, current_user["username"], collection)
            
        return Response(
            content=json.dumps({"message": "Answers, gender, and image URL saved successfully"}),
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    
@router.get("/all")
async def get_all_users(db_conn=Depends(get_db_conn)):
    collection = db_conn["user_data"]
    cursor = collection.find({}, {"_id": 0, "username": 1})
    users = await cursor.to_list(length=None)
    return {"users": users}


@router.get("/me")
async def get_current_user_info(current_user=Depends(get_current_user)):
    return {
        "username": current_user['username'],
        "selectedImage": getattr(current_user, "selectedImage", "boy_avatar1.png")
    }


@router.get("/recommendations")
async def get_recommendations(current_user=Depends(get_current_user), db_conn=Depends(get_db_conn)):
    collection = db_conn["user_data"]

    user_doc = await collection.find_one({"username": current_user["username"]})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    recommended_usernames = user_doc.get("recommended_users", [])
    detailed = []

    for uname in recommended_usernames:
        u = await collection.find_one({"username": uname})
        if u:
            detailed.append({
                "username": u["username"],
                "gender": u.get("gender", ""),
                "selectedImage": u.get("selectedImage", "")
            })

    return {"recommended_users": detailed}



@router.get("/by_username/{username}")
async def get_user_by_username(username: str, db=Depends(get_db_conn)):
    user = await db["user_data"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user["username"],
        "selectedImage": user.get("selectedImage", None),
    }