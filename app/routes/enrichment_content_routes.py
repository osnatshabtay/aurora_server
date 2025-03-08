from datetime import datetime
from app.modules.user import User
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.db import get_db_conn
import json
import logging
from app.services.users.session import get_current_user
from bson import ObjectId

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
        
        return Response(
            content=json.dumps({"answers": user_data["answers"]}, ensure_ascii=False), 
            status_code=200,
            media_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error retrieving user answers: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching user answers")