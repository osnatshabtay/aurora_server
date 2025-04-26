import logging
import pytest
import json
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn
from app.services.users.auth import get_current_user
from app.services.recommendations import classify_user_recom


class TestUserCategoryAndEnrichment:

    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)

            cls.mock_user = {"username": "israel"}

            cls.sample_answers = [
                {"question": "מה הוביל אותך להירשם לאפלקציה שלנו? ", "answers": "תחושת חרדה"},
                {"question": "האם חווית אירוע טראומטי?", "answers": "כן"}
            ]

        except Exception as e:
            logging.error(f"Error in setting up TestUserCategoryAndEnrichment class: {e}")
            raise Exception(f"Error in setting up TestUserCategoryAndEnrichment class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestUserCategoryAndEnrichment class: {e}")
            raise Exception(f"Error in tearing down TestUserCategoryAndEnrichment class: {e}")

    def test_classify_user_profile_from_db(self):
        profile = classify_user_recom.classify_user_profile_from_db(self.sample_answers)

        assert profile["anxiety"] is True
        assert profile["trauma"] is True
        assert profile["sleep_issues"] is False


    @pytest.mark.asyncio
    async def test_user_category(self, mock_db):

        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        await mock_db["user_data"].insert_one({
            "_id": 1,
            "username": "israel",
            "answers": self.sample_answers            
        })
        await mock_db["user_data"].insert_one({
            "_id": 2,
            "username": "bob",
            "answers": self.sample_answers,
            "classified_profile": {"trauma": True}     
        })


        response = self.client.post("/recommendations/user_category")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Updated 1 users with classified profile."


        israel_doc = await mock_db["user_data"].find_one({"username": "israel"})
        assert "classified_profile" in israel_doc
        assert israel_doc["classified_profile"]["anxiety"] is True
        assert israel_doc["classified_profile"]["trauma"] is True
        assert israel_doc["classified_profile"]["sleep_issues"] is False


    @pytest.mark.asyncio
    async def test_user_enrichment(self, mock_db):

        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        classified_profile = {"anxiety": True, "trauma": True}
        await mock_db["user_data"].insert_one({
            "username": "israel",
            "answers": self.sample_answers,
            "classified_profile": classified_profile
        })

        response = self.client.get("/recommendations/user_enrichment")
        assert response.status_code == 200

        data = response.json()
        assert data["classified_profile"] == classified_profile
