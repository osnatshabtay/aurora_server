import pytest
import logging
import asyncio
import json

from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn



class TestEntireFlow:

    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)
            cls.test_username = "ישראל ישראלי"
            cls.password = "123456!"
            
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

    @pytest.mark.asyncio
    async def test_good_register(self, mock_db):
        # Create a generator-based async override function
        async def override_get_db_conn():
            yield mock_db  # Directly yield the non-async mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        response = await self.register()
        assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"
        content = response.json()
        assert content['message'] == "User registered successfully", f"Unexpected message: {content['message']}"
        assert content['id'] is not None, "No ID supplied in response"

    @pytest.mark.asyncio
    async def test_register_with_existing_user(self, mock_db):
        async def override_get_db_conn():
            yield mock_db  # Directly yield the non-async mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        # Register user for the first time
        response = await self.register()
        assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"

        # Attempt to register the same user again
        response = await self.register()
        assert response.status_code == 400, f"Succeeded to register existing user. Response: {response.json()}"
        content = response.json()
        assert content['detail'] == "Username already exists.", f"Unexpected message: {content['detail']}"
    
    @pytest.mark.asyncio
    async def test_register_with_existing_user(self, mock_db):
        async def override_get_db_conn():
            yield mock_db  # Directly yield the non-async mock_db

        app.dependency_overrides[get_db_conn] = override_get_db_conn

        # Register user for the first time
        response = await self.register()
        assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"

        # Attempt to register the same user again
        response = await self.register()
        assert response.status_code == 400, f"Succeeded to register existing user. Response: {response.json()}"
        content = response.json()
        assert content['detail'] == "Username already exists.", f"Unexpected message: {content['detail']}"