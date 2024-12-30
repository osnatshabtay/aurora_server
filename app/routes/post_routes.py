from app.modules.post import Post
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.db import get_db_conn
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/write_post")
async def register_endpoint(post_input: Post, db_conn=Depends(get_db_conn)):
    collection = db_conn["post_data"]

    post = {
        'username': post_input.username,
        'text': post_input.text,
        'likes': list(post_input.likes),  
        'commands': [comment.dict() for comment in post_input.commands], 
        'approved': post_input.approved, 
    }

    existing_user = await db_conn['user_data'].find_one({"username": post_input.username})
    if not existing_user:
        logger.error(f"User '{post_input.username}' does not exist.")
        raise HTTPException(status_code=400, detail="Username not exists.")

    result = await collection.insert_one(post)
    if not result.acknowledged: 
        raise HTTPException(status_code=500, detail="Failed to save post to the database.")
    
    return Response(
        content=json.dumps({"message": "post successfully", "id": str(result.inserted_id)}),
        status_code=200
    )

@router.get("/all_posts")
async def questions_endpoint(db_conn=Depends(get_db_conn)):
    collection = db_conn["post_data"]

    posts_cursor = collection.find().sort("timestamp", -1)
    posts = await posts_cursor.to_list(length=None)  
    
    for post in posts:
        if "_id" in post:
            post["_id"] = str(post["_id"])

    return {"posts": posts}

