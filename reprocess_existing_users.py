import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from app.models.social_graph import process_questionnaire_answers

# טען משתנים מתוך .env
load_dotenv()

# שלוף פרטי התחברות
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
uri_template = os.getenv("MONGO_URI")

# בנה URI תקף
MONGO_URI = uri_template.replace("<db_password>", password)
DB_NAME = "aurora-database"

async def main():
    print("🔌 Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["user_data"]

    print("🔍 Fetching users with answers...")
    success_count = 0
    fail_count = 0

    async for user in users_collection.find({"answers": {"$exists": True}}):
        username = user["username"]
        try:
            print(f"⏳ Processing {username}...")
            await process_questionnaire_answers(
                {"answers": user["answers"]},
                username,
                users_collection
            )
            print(f"✅ Done: {username}")
            success_count += 1
        except Exception as e:
            import traceback
            print(f"❌ Failed for {username}: {type(e).__name__} - {e}")
            traceback.print_exc()
            fail_count += 1


    print(f"\n✅ Finish: {success_count} Sucess | ❌ {fail_count} Failed")

if __name__ == "__main__":
    asyncio.run(main())
