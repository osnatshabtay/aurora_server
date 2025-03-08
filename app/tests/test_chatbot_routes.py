import logging
import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_conn
from app.services.users.session import get_current_user
from app.modules.message import Message
import app.openai as openai_handler

class TestChatbotRoutes:

    @classmethod
    def setup_class(cls):
        try: 
            cls.client = TestClient(app)
            cls.mock_user = {
                    "username": "test_user",
                    "selectedImage": "test_image_url",
                }
            cls.message = {"message": "Hi :)"}
        except Exception as e:
            logging.error(f"Error in setting up TestChatbotRoutes class: {e}")
            raise Exception(f"Error in setting up TestChatbotRoutes class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestChatbotRoutes class: {e}")
            raise Exception(f"Error in tearing down TestChatbotRoutes class: {e}")

    @pytest.fixture
    def mock_openai_handler(self, monkeypatch):
        mock_handler = AsyncMock()
        mock_client = AsyncMock()
        mock_handler.get_async_client.return_value = mock_client
        mock_handler.chat_completion.return_value = "Mocked response!"
        mock_handler.chat_completion_with_history.return_value = ("Mocked response!", [])
        monkeypatch.setattr(openai_handler, "get_async_client", AsyncMock(return_value=mock_client))
        monkeypatch.setattr(openai_handler, "chat_completion", AsyncMock(return_value="Mocked response!"))
        monkeypatch.setattr(openai_handler, "chat_completion_with_history", AsyncMock(return_value=("Mocked response!", [])))
        return mock_handler

    @pytest.mark.asyncio
    async def test_chat_no_history(self, mock_openai_handler, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        await mock_db["user_data"].insert_one(self.mock_user)

        response = self.client.post("/chatbot/chat_no_history", json=self.message)
        assert response.status_code == 200
        data = response.json()
        assert "Mocked response!" in data.get("response", "")

    @pytest.mark.asyncio
    async def test_chat_with_history(self, mock_openai_handler, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        await mock_db["user_data"].insert_one({"username": self.mock_user["username"], "chat_history": [{"role": "user", "content": "Hi"}]})

        response = self.client.post("/chatbot/chat_with_history", json=self.message)
        assert response.status_code == 200
        data = response.json()
        assert "Mocked response!" in data.get("response", "")

    @pytest.mark.asyncio
    async def test_get_chat_history(self, mock_db):
        async def override_get_db_conn():
            yield mock_db

        async def override_get_current_user():
            return self.mock_user

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        app.dependency_overrides[get_current_user] = override_get_current_user

        chat_history_mock = [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]
        await mock_db["user_data"].insert_one({"username": self.mock_user["username"], "chat_history": chat_history_mock})

        response = self.client.get("/chatbot/chat_history")
        assert response.status_code == 200
        data = response.json()
        assert data.get("chat_history") == chat_history_mock


