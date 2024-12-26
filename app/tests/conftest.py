import pytest
from mongomock_motor import AsyncMongoMockClient

@pytest.fixture(scope="function")
async def mock_db():
    # Use a mock MongoDB instance
    client = AsyncMongoMockClient()
    db = client["test_mock_database"]
    yield db
    client.close()