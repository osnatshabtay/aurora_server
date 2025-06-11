from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from jose import jwt, JWTError
from app.services.users.auth import SECRET_KEY, ALGORITHM
from app.db import get_db_conn
import os
from fastapi import Body
from app.services.users.auth import get_current_user
from typing import List
from fastapi import Query



router = APIRouter()

active_connections: dict[str, WebSocket] = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db_conn=Depends(get_db_conn)):
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user = await get_user_from_token(token, db_conn)
        username = user["username"]
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    active_connections[username] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            to_user = data["to"]
            message_text = data["message"]

            message = {
                "from": username,
                "to": to_user,
                "message": message_text,
                "timestamp": datetime.utcnow().isoformat(),
                "seen": False
            }
            
            messages_collection = db_conn["messages"]
            print("saving message:", message)
            await messages_collection.insert_one(message)

            if to_user in active_connections:
                await active_connections[to_user].send_json(message)

    except WebSocketDisconnect:
        del active_connections[username]


@router.get("/chat/{user1}/{user2}")
async def get_messages(user1: str, user2: str, db_conn=Depends(get_db_conn)):
    try:
        messages_collection = db_conn["messages"]
        query = {
            "$or": [
                {"from": user1, "to": user2},
                {"from": user2, "to": user1}
            ]
        }
        cursor = messages_collection.find(query, {"_id": 0})
        messages = [msg async for msg in cursor]
        messages.sort(key=lambda x: x["timestamp"])
        return messages
    except Exception as e:
        print("Error fetching chat messages:", e)
        raise HTTPException(status_code=500, detail=str(e))


async def get_user_from_token(token: str, db_conn):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise ValueError("Missing username in token")
        user = await db_conn["user_data"].find_one({"username": username})
        if not user:
            raise ValueError("User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/chat/mark_seen")
async def mark_messages_as_seen(
    from_user: str = Body(...),
    to_user: str = Body(...),
    db_conn=Depends(get_db_conn)
):
    messages_collection = db_conn["messages"]
    result = await messages_collection.update_many(
        {"from": from_user, "to": to_user, "seen": False},
        {"$set": {"seen": True}}
    )
    return {"updated_count": result.modified_count}

@router.get("/chat/unread")
async def get_unread_messages(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):    
    collection = db_conn["messages"]
    messages = await collection.find({
        "to": current_user["username"],
        "seen": False
    }, {"_id": 0}).to_list(length=None)

    return {
        "count": len(messages),
        "messages": messages
    }

@router.get("/users/multiple")
async def get_multiple_users(usernames: List[str] = Query(...), db_conn=Depends(get_db_conn)):
    users_collection = db_conn["user_data"]
    cursor = users_collection.find(
        {"username": {"$in": usernames}},
        {"_id": 0, "username": 1, "selectedImage": 1}
    )
    users = await cursor.to_list(length=None)
    print(users)
    return users    