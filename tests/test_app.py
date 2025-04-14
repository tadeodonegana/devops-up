# tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import os
import sys

# Set a mock API key for testing
os.environ["GROQ_API_KEY"] = "mock-api-key-for-testing"

# Now import the app
from main import app

client = TestClient(app)

class MockResponse:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

@patch('services.client.chat.completions.create')
def test_recommendations_endpoint(mock_create):
    # Mock the LLM response
    mock_create.return_value = MockResponse({"recommended_items": ["garlic", "olive oil", "basil"]})
    
    payload = {"products": ["pasta", "tomato sauce"]}
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_items" in data
    assert isinstance(data["recommended_items"], list)

@patch('services.client.chat.completions.create')
def test_dish_ingredients_endpoint(mock_create):
    # Mock the LLM response
    mock_create.return_value = MockResponse({"ingredients": ["chickpeas", "tahini", "lemon juice", "olive oil"]})
    
    response = client.get("/dishes/ingredients", params={"dish_name": "hummus"})
    assert response.status_code == 200
    data = response.json()
    assert "ingredients" in data
    assert isinstance(data["ingredients"], list)

@patch('services.client.chat.completions.create')
def test_categorize_products_endpoint(mock_create):
    # Mock the LLM response
    mock_categories = {
        "dairy": ["cheese", "yogurt", "milk"],
        "bakery": ["baguette"]
    }
    mock_create.return_value = MockResponse({"categories": mock_categories})
    
    payload = {
        "uncategorized_products": ["yogurt", "baguette", "milk"],
        "categorized_products": {"dairy": ["cheese"], "bakery": []}
    }
    response = client.post("/categorize-products", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert isinstance(data["categories"], dict)
