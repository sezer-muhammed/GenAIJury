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

def test_get_unique_names_multiple(mongo_interface):
    # Test for multiple unique names in the JSON file
    documents = [
        {"Name": "Name 1"},
        {"Name": "Name 2"},
        {"Name": "Name 3"},
        {"Name": "Name 1"},  # Repeat Name 1
        {"Name": "Name 4"},
        {"Name": "Test Entity", "Criterias": {"Criteria1": 100, "Criteria2": 90}}
    ]
    for doc in documents:
        mongo_interface.create(doc)
    expected_unique_names = ["Name 1", "Name 2", "Name 3", "Name 4", "Test Entity"]
    assert sorted(mongo_interface.get_unique_names()) == sorted(expected_unique_names)