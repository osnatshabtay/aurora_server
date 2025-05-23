import pytest
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn

from bson import ObjectId

class TestAdminPostRoutes:

    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)
            cls.test_username = "admin_user"
            cls.password = "Admin123!"
            cls.post_text = "Pending post for approval."
            cls.mock_post = {
                "_id": ObjectId(),
                "user": "admin_user",
                "user_image": "admin_image_url",
                "text": "Pending post for approval.",
                "approved": False,
            }
        except Exception as e:
            logging.error(f"Error in setting up TestAdminPostRoutes class: {e}")
            raise Exception(f"Setup error: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestAdminPostRoutes class: {e}")
            raise Exception(f"Teardown error: {e}")

    @pytest.mark.asyncio
    async def test_pending_posts_success(self, mock_db):
        async def override_get_db_conn():
            yield mock_db
        app.dependency_overrides[get_db_conn] = override_get_db_conn

        await mock_db["post_data"].insert_one(self.mock_post)

        response = self.client.get("/feed/pending_posts")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        content = response.json()
        assert "pending_posts" in content, "No pending_posts in response"
        assert isinstance(content["pending_posts"], list), "pending_posts is not a list"
        assert any(post["text"] == self.post_text for post in content["pending_posts"]), "Inserted post not found"

    @pytest.mark.asyncio
    async def test_approve_post_success(self, mock_db):
        async def override_get_db_conn():
            yield mock_db
        app.dependency_overrides[get_db_conn] = override_get_db_conn

        inserted_post = await mock_db["post_data"].insert_one(self.mock_post)

        response = self.client.put(f"/feed/approve_post/{str(self.mock_post['_id'])}")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        content = response.json()
        assert content["message"] == "Post approved successfully", "Unexpected message returned"

        # verify in DB
        updated_post = await mock_db["post_data"].find_one({"_id": self.mock_post["_id"]})
        assert updated_post["approved"] is True, "Post not marked as approved"

    @pytest.mark.asyncio
    async def test_approve_post_not_found(self, mock_db):
        async def override_get_db_conn():
            yield mock_db
        app.dependency_overrides[get_db_conn] = override_get_db_conn

        fake_id = str(ObjectId())
        response = self.client.put(f"/feed/approve_post/{fake_id}")

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert content["detail"] == "Post not found", "Unexpected detail message"

    @pytest.mark.asyncio
    async def test_delete_post_success(self, mock_db):
        async def override_get_db_conn():
            yield mock_db
        app.dependency_overrides[get_db_conn] = override_get_db_conn

        inserted_post = await mock_db["post_data"].insert_one(self.mock_post)

        response = self.client.delete(f"/feed/delete_post/{str(self.mock_post['_id'])}")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        content = response.json()
        assert content["message"] == "Post deleted successfully", "Unexpected message returned"

        # Verify post actually deleted
        deleted_post = await mock_db["post_data"].find_one({"_id": self.mock_post["_id"]})
        assert deleted_post is None, "Post was not actually deleted"

    @pytest.mark.asyncio
    async def test_delete_post_not_found(self, mock_db):
        async def override_get_db_conn():
            yield mock_db
        app.dependency_overrides[get_db_conn] = override_get_db_conn

        fake_id = str(ObjectId())
        response = self.client.delete(f"/feed/delete_post/{fake_id}")

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert content["detail"] == "Post not found", "Unexpected detail message"
