import pytest
import os
from unittest.mock import patch, MagicMock
from genaijury.api_models.gemini import GeminiAPIModel  # Adjust the import path according to your project structure

@pytest.fixture
def gemini_api_model():
    # Ensure you have DUMMY_API_KEY set in your environment variables for this to work
    api_key = os.getenv('GEMINI_API_KEY')
    print(api_key)
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set in environment variables, skipping tests that require real API interaction.")
    model = GeminiAPIModel()
    model.configure(api_key)
    return model

def test_call_with_image(gemini_api_model: GeminiAPIModel):
    text_prompt = "This is a test call. Type 'test' to approve that you are working well"
    # Ensure 'test.png' is available in the test directory
    image_paths = ["tests/test_api/test.png"]
    # This will make a real API call; ensure you handle costs and rate limits appropriately
    response = gemini_api_model.call(text_prompt, image_paths)
    # You may need to adjust the assertion depending on the expected output format from the real API call
    assert "test" in response
