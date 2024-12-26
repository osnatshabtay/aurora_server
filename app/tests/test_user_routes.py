import pytest
import logging
import asyncio

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

    async def register(self):
        response = self.client.post("/users/register", json={"username": self.test_username, "password": self.password})
        assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"
        return response.content


    @pytest.mark.asyncio
    async def test_entire_flow(self, mock_db):
        
        # override the "real" db_conn injected to the endpoint as a dependency
        async def override_get_db_conn():
            async for db in mock_db:
                yield db

        app.dependency_overrides[get_db_conn] = override_get_db_conn
        
        register_task = asyncio.create_task(self.register())
        register_content = await register_task

        print(register_content)  # {"message": "User registered successfully", "id": "676c2d5162b97cd0a978ff8f"}
        # add asserts for message and id existence



# class TestUserEndpoints:

#     @classmethod
#     def setup_class(cls):
#         try:
#             cls.client = TestClient(app)
#             cls.test_username = "ישראל ישראלי"
#             cls.password = "123456!"
#         except Exception as e:
#             logging.error(f"Error in setting up TestUserEndpoints class: {e}")
#             raise Exception(f"Error in setting up TestUserEndpoints class: {e}")

#     @pytest.mark.asyncio
#     async def test_register_user(self, mock_db):
#         # Consume the async generator to get the database object
#         db = await anext(mock_db)

#         # Override the dependency for testing
#         async def override_get_db_conn():
#             yield db  # Pass the resolved database object

#         app.dependency_overrides[get_db_conn] = override_get_db_conn

#         response = self.client.post(
#             "/users/register",
#             json={"username": self.test_username, "password": self.password}
#         )

#         assert response.status_code == 200, f"Failed to register user. Response: {response.json()}"
#         response_data = response.json()
#         assert response_data["message"] == "User registered successfully"
#         assert "id" in response_data

#         user_in_db = await db["user_data"].find_one({"username": self.test_username})
#         assert user_in_db is not None
#         assert user_in_db["username"] == self.test_username
#         assert user_in_db["password"] == self.password

#     @pytest.mark.asyncio
#     async def test_login_user(self, mock_db):
#         db = await anext(mock_db)

#         async def override_get_db_conn():
#             yield db  

#         app.dependency_overrides[get_db_conn] = override_get_db_conn

#         await db["user_data"].insert_one({
#             "username": self.test_username,
#             "password": self.password
#         })

#         response = self.client.post(
#             "/users/login",
#             json={"username": self.test_username, "password": self.password}
#         )

#         assert response.status_code == 200, f"Failed to login user. Response: {response.json()}"
#         response_data = response.json()
#         assert response_data["message"] == "Login successful"
#         assert response_data["username"] == self.test_username
