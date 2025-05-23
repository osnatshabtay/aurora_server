from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.db import get_db_conn
import json
import logging
import app.openai as openai_handler
from app.modules.message import Message
from app.services.users.auth import get_current_user



logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat_no_history")
async def chat(message_input: Message):
    client = None
    try:
        client = openai_handler.get_async_client()

        resp = await openai_handler.chat_completion(client, message_input.message)
    
        return Response(
                content=json.dumps({"response": resp}),
                status_code=200
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    finally:
        if client:
            client.close()
    
@router.post("/chat_with_history")
async def chat(message_input: Message, db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):
    client = None

    user_data = await db_conn["user_data"].find_one({"username": current_user["username"]})
    if not user_data:
        raise HTTPException(status_code=400, detail="User does not exist.")

    chat_history = user_data.get("chat_history", [])
    
    try:
        client= openai_handler.get_async_client()

        if chat_history:
            resp, updated_history = await openai_handler.chat_completion_with_history(client, chat_history, message_input.message)
        else:
            resp = await openai_handler.chat_completion(client, message_input.message)
            updated_history = [{"role": "user", "content": message_input.message}, {"role": "assistant", "content": resp}]
    
        updated_history = updated_history[-10:] 

        await db_conn["user_data"].update_one(
            {"username": current_user["username"]},
            {"$set": {"chat_history": updated_history}}
        )
        return {"response": resp}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    finally:
        if client:
            client.close()
    
@router.get("/chat_history")
async def get_chat_history(db_conn=Depends(get_db_conn), current_user=Depends(get_current_user)):

    username = current_user["username"]
    user_data = await db_conn["user_data"].find_one({"username": username})

    if not user_data:
        raise HTTPException(status_code=400, detail="User does not exist.")

    # Retrieve chat history
    chat_history = user_data.get("chat_history", [])

    return {"username": username, "chat_history": chat_history}
