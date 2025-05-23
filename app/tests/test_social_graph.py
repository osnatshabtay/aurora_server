import pytest
from mongomock_motor import AsyncMongoMockClient
from app.models.social_graph import process_questionnaire_answers

@pytest.mark.asyncio
async def test_process_questionnaire_answers_adds_fields():
    # יצירת דאטאבייס מדומה
    client = AsyncMongoMockClient()
    db = client["test-database"]
    users_collection = db["user_data"]

    # הוספת משתמש עם תשובות
    await users_collection.insert_one({
        "username": "TestUser",
        "answers": ["I feel anxious", "I like nature", "I enjoy meditation"]
    })

    # קריאה לפונקציה האסינכרונית
    await process_questionnaire_answers(
        {"answers": ["I feel anxious", "I like nature", "I enjoy meditation"]},
        "TestUser",
        users_collection
    )

    # שליפת המשתמש לבדיקה
    updated_user = await users_collection.find_one({"username": "TestUser"})

    # בדיקות
    assert "embedding" in updated_user, "שדה embedding לא נוסף למשתמש"
    assert "cluster_id" in updated_user, "שדה cluster_id לא נוסף למשתמש"
    assert "recommended_users" in updated_user, "שדה recommended_users לא נוסף למשתמש"
    assert isinstance(updated_user["recommended_users"], list), "recommended_users לא מסוג list"
