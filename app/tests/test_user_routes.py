import pytest
import logging
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn

class TestEntireFlow:

    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)
            cls.test_username = "ישראל ישראלי"
            cls.password = "123456O!"

            cls.mock_questions = [
                {"_id": "1", "question": "What is 2+2?", "options": ["3", "4", "5"], "answer": "4"},
                {"_id": "2", "question": "What is 3+3?", "options": ["5", "6", "7"], "answer": "6"}
            ]
            cls.answers = {"answer1": "4", "answer2": "6"}
            
        except Exception as e:
            logging.error(f"Error in setting up TestEntireFlow class: {e}")
            raise Exception(f"Error in setting up TestEntireFlow class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestEntireFlow class: {e}")
            raise Exception(f"Error in tearing down TestEntireFlow class: {e}")

    async def register(self, username=None, password=None):
        if username is None or password is None:
            response = self.client.post("/users/register", json={"username": self.test_username, "password": self.password})
        else:
            response = self.client.post("/users/register", json={"username": username, "password": password})

        return response
    
    async def login(self, username, password):
        response = self.client.post("/users/login", json={"username": username, "password": password})
        return response
    
    @pytest.mark.asyncio
    async def test_good_register(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        response = await self.register()
        assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"
        content = response.json()
        
        assert 'access_token' in content, "access_token missing in response"
        assert 'token_type' in content, "token_type missing in response"

    @pytest.mark.asyncio
    async def test_register_with_existing_user(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        # First register
        response = await self.register()
        assert response.status_code == 200

        # Try registering again
        response = await self.register()
        assert response.status_code == 400, f"Expected 400 for existing user. Response: {response.json()}"
        content = response.json()
        assert content['detail'] == "Username already exists.", f"Wrong detail: {content['detail']}"

    
    # ----------------- login -----------------
    @pytest.mark.asyncio
    async def test_good_login(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        await self.register(username=self.test_username, password=self.password)

        response = await self.login(username=self.test_username, password=self.password)
        assert response.status_code == 200, f"Unable to login with existing user. Response: {response.json()}"
        
        content = response.json()
        assert 'access_token' in content, "access_token missing in login response"
        assert 'token_type' in content, "token_type missing in login response"
        assert 'is_admin' in content, "is_admin missing in login response"

    @pytest.mark.asyncio
    async def test_login_bad_password(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        await self.register(username=self.test_username, password=self.password)

        response = await self.login(username=self.test_username, password=f"{self.password}wrong")
        assert response.status_code == 401, f"Expected 401 for bad password. Response: {response.json()}"
        
        content = response.json()
        assert content['detail'] == "Invalid username or password.", f"Wrong detail: {content['detail']}"

    @pytest.mark.asyncio
    async def test_login_bad_username(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        response = await self.login(username="nonexistent_user", password=self.password)
        assert response.status_code == 401, f"Expected 401 for bad username. Response: {response.json()}"
        
        content = response.json()
        assert content['detail'] == "Invalid username or password.", f"Wrong detail: {content['detail']}"


    # # ----------------- questions -----------------
    # @pytest.mark.asyncio
    # async def test_post_questions(self, mock_db):
    #     async def override_get_db_conn():
    #         yield mock_db

    #     app.dependency_overrides[get_db_conn] = override_get_db_conn

    #     global current_user
    #     current_user = type("User", (object,), {"username": "test_user"})()

    #     response = self.client.post("/users/questions", json=self.answers, is_test=True)

    #     assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    #     assert response.json()["message"] == "Answers, gender, and image URL saved successfully", f"Unexpected message: {response.json()['message']}"


    