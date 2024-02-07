import pytest
import os
from genaijury.database.json import JSONFileInterface

# Path to a temporary JSON file for testing
TEST_JSON_PATH = "test_database.json"

@pytest.fixture(scope="module")
def json_interface():
    # Setup JSON file interface for testing
    interface = JSONFileInterface(TEST_JSON_PATH)
    yield interface
    # Teardown: Remove test JSON file after tests
    os.remove(TEST_JSON_PATH)

def test_create(json_interface):
    document = {"Name": "Test Entity", "Criterias": {"Criteria1": 100, "Criteria2": 90}}
    index = json_interface.create(document)
    assert index == 0  # First document

def test_read(json_interface):
    query = {"Name": "Test Entity"}
    results = json_interface.read(query)
    assert len(results) > 0
    assert results[0]["Criterias"]["Criteria1"] == 100

def test_update(json_interface):
    query = {"Name": "Test Entity"}
    new_data = {"Criterias": {"Criteria1": 95}}  # Assume we're updating the score for Criteria1
    updated_count = json_interface.update(query, new_data)
    assert updated_count > 0

def test_delete(json_interface):
    query = {"Name": "Test Entity"}
    deleted_count = json_interface.delete(query)
    assert deleted_count > 0
