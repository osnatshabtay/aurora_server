import os
from openai import AsyncOpenAI

def get_async_client():
    try:
        client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        return client
    except Exception as e:
        print(f"Error getting async client for OpenAI: {e}")
        raise e
    

async def chat_completion_with_history(client, message_history, new_message, max_messages_history=10):
    """
    Handles conversation history while generating responses.
    """
    try:
        # Append the new user message to the history
        if len(message_history) > max_messages_history:
            message_history = message_history[-max_messages_history:]

        message_history.append({"role": "user", "content": new_message})

        # Call OpenAI API with conversation history
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=message_history
        )

        # get response
        resp = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": resp})

        return resp, message_history
    except Exception as e:
        print(f"Error in chat_completion_with_history: {e}")
        return "An error occurred, please try again later."


async def chat_completion(client, user_prompt, system_prompt=None):
    """
    Generates a single response based on a user prompt with an optional system instruction.
    """
    try:
        messages = []

        # Include system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add user message
        messages.append({"role": "user", "content": user_prompt})

        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        resp = response.choices[0].message.content
        print(f"chat resp = {resp}")
        return resp
    
    except Exception as e:
        print(f"Error in chat_completion: {e}")
        return "An error occurred, please try again later."
