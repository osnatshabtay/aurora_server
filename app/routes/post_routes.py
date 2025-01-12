from datetime import datetime
from app.modules.post import Post, LikeRequest, Comment, CommentRequest
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

@router.post("/write_post")
async def write_post_endpoint(post_input: Post, db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    collection = db_conn["post_data"]

    if not isinstance(current_user, dict):
        current_user = current_user.dict()

    existing_user = await db_conn["user_data"].find_one({"username": current_user["username"]})
    if not existing_user:
        raise HTTPException(status_code=400, detail="User does not exist.")

    new_post = Post(
        user=current_user["username"],
        user_image=current_user.get("selectedImage", ""),
        text=post_input.text
    )

    post_dict = new_post.dict()
    result = await collection.insert_one(post_dict)

    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to save post to the database.")

    return Response(
        content=json.dumps({"message": "Post created successfully", "id": str(result.inserted_id)}),
        status_code=200
    )

@router.get("/all_posts")
async def posts_endpoint(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    collection = db_conn["post_data"]

    posts_cursor = collection.find().sort("timestamp", -1)
    posts = await posts_cursor.to_list(length=None)

    for post in posts:
        if "_id" in post:
            post["_id"] = str(post["_id"])
    
    if not isinstance(current_user, dict):
        current_user = current_user.dict()

    return {"posts": posts, "current_username": current_user["username"], "current_username_image": current_user["selectedImage"] }


@router.post("/like")
async def like_endpoint(request: LikeRequest, db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    
    post_id = request.post_id
    collection = db_conn["post_data"]

    if not isinstance(current_user, dict):
        current_user = current_user.dict()

    username = current_user["username"]

    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post_id format.")

    try:

        post = await collection.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found.")

        #unlike
        if username in post["likes"]:
            await collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"likes": username}}
            )
            message = "Like removed."
        else:
            #like
            await collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$addToSet": {"likes": username}}
            )
            message = "Like added."

        return Response(
            content=json.dumps({"message": message}),
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.post("/comment")
async def comments_endpoint(request: CommentRequest, db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    collection = db_conn["post_data"]

    if not isinstance(current_user, dict):
        current_user = current_user.dict()

    username = current_user["username"]

    if not ObjectId.is_valid(request.post_id):
        raise HTTPException(status_code=400, detail="Invalid post_id format.")

    try:
        post = await collection.find_one({"_id": ObjectId(request.post_id)})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found.")

        comment = {
            "username": username,
            "text": request.text,
            "timestamp": datetime.utcnow()
        }

        await collection.update_one(
            {"_id": ObjectId(request.post_id)},
            {"$push": {"commands": comment}}
        )

        return Response(
            content=json.dumps({"message": "Comment added successfully!"}),
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
