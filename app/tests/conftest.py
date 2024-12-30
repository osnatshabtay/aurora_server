import pytest
from mongomock_motor import AsyncMongoMockClient

@pytest.fixture(scope="function")
def mock_db():
    # Use a non-async fixture to avoid async generator conflicts
    client = AsyncMongoMockClient()
    db = client["test_mock_database"]
    yield db  # Yield the database instance
    client.close()  # Ensure cleanup after each test

