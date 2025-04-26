import pytest
import logging
import json
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn
from app.services.users.auth import get_current_user

class TestPostRoutes:
    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)
            cls.test_username = "ישראל ישראלי"
            cls.password = "123456O!"
            cls.post_text = "This is a test post."

            cls.mock_user = {
                "username": cls.test_username,
                "selectedImage": "test_image_url",
            }

            cls.mock_post = {
                "user": cls.test_username,
                "user_image": "test_image_url",
                "text": cls.post_text,
            }

        except Exception as e:
            logging.error(f"Error in setting up TestPostRoutes class: {e}")
            raise Exception(f"Error in setting up TestPostRoutes class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestPostRoutes class: {e}")
            raise Exception(f"Error in tearing down TestPostRoutes class: {e}")

    # ----------------- write_post -----------------
    @pytest.mark.asyncio
    async def test_write_post_success(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        await mock_db["user_data"].insert_one(self.mock_user)

        response = self.client.post("/feed/write_post", json={"text": self.post_text})

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert content["message"] == "Post created successfully", f"Unexpected message: {content['message']}"
        assert "id" in content, "Post ID not returned in response"

    @pytest.mark.asyncio
    async def test_write_post_user_not_found(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        response = self.client.post("/feed/write_post", json={"text": self.post_text})

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert content["detail"] == "User does not exist.", f"Unexpected message: {content['detail']}"


    # ----------------- all_posts -----------------
    @pytest.mark.asyncio
    async def test_all_posts_success(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        await mock_db["user_data"].insert_one(self.mock_user)
        await mock_db["post_data"].insert_one(self.mock_post)

        response = self.client.get("/feed/all_posts")

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert "posts" in content, "Posts not returned in response"
        assert content["current_username"] == self.test_username, f"Unexpected username: {content['current_username']}"
        assert content["current_username_image"] == "test_image_url", f"Unexpected user image: {content['current_username_image']}"

    @pytest.mark.asyncio
    async def test_all_posts_no_posts(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        response = self.client.get("/feed/all_posts")

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        content = response.json()
        assert content["posts"] == [], "Posts list is not empty"
        assert content["current_username"] == self.test_username, f"Unexpected username: {content['current_username']}"
        assert content["current_username_image"] == "test_image_url", f"Unexpected user image: {content['current_username_image']}"
