import pytest
from genaijury.database.mongo import MongoDBInterface
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Configuration for MongoDB test database
TEST_DB_URI = "mongodb://localhost:27017/"
TEST_DB_NAME = "test_database"
TEST_COLLECTION_NAME = "test_collection"

@pytest.fixture(scope="module")
def mongo_interface():
    # Setup MongoDB interface for testing
    interface = MongoDBInterface(TEST_DB_URI, TEST_DB_NAME, TEST_COLLECTION_NAME)
    yield interface
    # Teardown: Drop test collection after tests
    client = MongoClient(TEST_DB_URI)
    client[TEST_DB_NAME].drop_collection(TEST_COLLECTION_NAME)

def test_connect(mongo_interface):
    # Attempt to connect to MongoDB. This will raise an exception if unsuccessful.
    try:
        mongo_interface.connect()
        connected = True
    except ServerSelectionTimeoutError:
        connected = False
    assert connected

def test_create(mongo_interface):
    document = {"Name": "Test Entity", "Criterias": {"Criteria1": 100, "Criteria2": 90}}
    inserted_id = mongo_interface.create(document)
    assert inserted_id is not None

def test_read(mongo_interface):
    query = {"Name": "Test Entity"}
    results = mongo_interface.read(query)
    assert len(results) > 0
    assert results[0]["Criterias"]["Criteria1"] == 100

def test_update(mongo_interface):
    query = {"Name": "Test Entity"}
    new_data = {"Criterias": {"Criteria1": 95}}  # Update the score for Criteria1
    updated_count = mongo_interface.update(query, new_data)
    assert updated_count > 0

def test_delete(mongo_interface):
    query = {"Name": "Test Entity"}
    deleted_count = mongo_interface.delete(query)
    assert deleted_count > 0
