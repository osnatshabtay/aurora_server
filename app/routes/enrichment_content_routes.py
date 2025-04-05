from datetime import datetime
from app.modules.user import User
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.db import get_db_conn
import json
import logging
from app.services.users.session import get_current_user
from bson import ObjectId 
from app.services.recommendations import classify_user_recom
from app.services.recommendations.content_data import personalized_content


logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/user_question")
async def user_question(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):

    if not current_user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    
    if not isinstance(current_user, dict):
        current_user = current_user.dict()
    
    collection = db_conn["user_data"]
    
    try:
        user_data = await collection.find_one({"username": current_user["username"]}, {"answers": 1, "_id": 0})
        
        if not user_data or "answers" not in user_data:
            raise HTTPException(status_code=404, detail="No answers found for this user")
        
        classified_profile = classify_user_recom.classify_user_profile_from_db(user_data["answers"])

        return Response(
            content=json.dumps({
                "answers": user_data["answers"],
                "classified_profile": classified_profile
            }, ensure_ascii=False), 
            status_code=200,
            media_type="application/json"
        )

    except Exception as e:
        logger.error(f"Error retrieving user answers: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching user answers")
  
    

@router.post("/user_category")
async def user_category(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="User is not authenticated")

    if not isinstance(current_user, dict):
        current_user = current_user.dict()

    collection = db_conn["user_data"]

    try:
        users = collection.find({"answers": {"$exists": True}})
        updated_count = 0

        async for user in users:
            if "classified_profile" not in user:
                answers = user["answers"]
                classified_profile = classify_user_recom.classify_user_profile_from_db(answers)

                await collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"classified_profile": classified_profile}}
                )
                updated_count += 1

        return {"message": f"Updated {updated_count} users with classified profile."}

    except Exception as e:
        logger.error(f"Error updating user categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user categories")

@router.get("/user_enrichment")
async def get_user_enrichment(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    
    if not isinstance(current_user, dict):
        current_user = current_user.dict()
    
    collection = db_conn["user_data"]

    try:
        user_data = await collection.find_one(
            {"username": current_user["username"]}, 
            {"classified_profile": 1, "_id": 0}
        )

        if not user_data or "classified_profile" not in user_data:
            raise HTTPException(status_code=404, detail="No classified profile found for this user")
        
        profile = user_data["classified_profile"]
        
        # נשלוף רק את הקטגוריות שהן True
        relevant_categories = [key for key, val in profile.items() if val is True]

        # בנה את המידע המותאם לפי הקטגוריות
        personalized_result = {
            cat: personalized_content.get(cat, []) for cat in relevant_categories
        }

        return Response(
            content=json.dumps({
                "classified_profile": profile,
                "personalized_content": personalized_result
            }, ensure_ascii=False), 
            status_code=200,
            media_type="application/json"
        )

    except Exception as e:
        logger.error(f"Error retrieving user enrichment content: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching enrichment content")
