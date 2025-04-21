# tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import os

os.environ["GROQ_API_KEY"] = "mock-api-key-for-testing"

from main import app

client = TestClient(app)

class TestBackendAPI(unittest.TestCase):
    """Test class for the Backend API endpoints"""

    def setUp(self):
        """Setup method that runs before each test"""
        # Setup test client
        self.client = client

    @patch('services.client.chat.completions.create')
    def test_recommendations_endpoint_success(self, mock_create):
        """Test successful recommendations endpoint response"""
        # Mock the LLM response with explicit response structure
        expected_items = ["garlic", "olive oil", "basil", "oregano"]
        mock_create.return_value = MagicMock(recommended_items=expected_items)
        
        # Test with sample products
        payload = {"products": ["pasta", "tomato sauce"]}
        response = self.client.post("/recommendations", json=payload)
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_items", data)
        self.assertIsInstance(data["recommended_items"], list)
        self.assertEqual(data["recommended_items"], expected_items)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()

    @patch('services.client.chat.completions.create')
    def test_recommendations_endpoint_error(self, mock_create):
        """Test recommendations endpoint with error response"""
        # Mock LLM service raising an exception
        mock_create.side_effect = Exception("API Error")
        
        payload = {"products": ["pasta", "tomato sauce"]}
        response = self.client.post("/recommendations", json=payload)
        
        # Verify error response
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Failed to get recommendations")

    @patch('services.client.chat.completions.create')
    def test_dish_ingredients_endpoint_success(self, mock_create):
        """Test successful dish ingredients endpoint response"""
        # Mock the LLM response
        expected_ingredients = ["chickpeas", "tahini", "lemon juice", "olive oil", "garlic"]
        mock_create.return_value = MagicMock(ingredients=expected_ingredients)
        
        # Test with sample dish
        response = self.client.get("/dishes/ingredients", params={"dish_name": "hummus"})
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ingredients", data)
        self.assertIsInstance(data["ingredients"], list)
        self.assertEqual(data["ingredients"], expected_ingredients)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()

    @patch('services.client.chat.completions.create')
    def test_dish_ingredients_endpoint_error(self, mock_create):
        """Test dish ingredients endpoint with error response"""
        # Mock LLM service raising an exception
        mock_create.side_effect = Exception("API Error")
        
        response = self.client.get("/dishes/ingredients", params={"dish_name": "hummus"})
        
        # Verify error response
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Failed to get dish ingredients")

    @patch('services.client.chat.completions.create')
    def test_categorize_products_endpoint_success(self, mock_create):
        """Test successful product categorization endpoint response"""
        # Mock the LLM response
        expected_categories = {
            "dairy": ["cheese", "yogurt", "milk"],
            "bakery": ["baguette"]
        }
        mock_create.return_value = MagicMock(categories=expected_categories)
        
        # Test with sample categorized and uncategorized products
        payload = {
            "uncategorized_products": ["yogurt", "baguette", "milk"],
            "categorized_products": {"dairy": ["cheese"], "bakery": []}
        }
        response = self.client.post("/categorize-products", json=payload)
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("categories", data)
        self.assertIsInstance(data["categories"], dict)
        self.assertEqual(data["categories"], expected_categories)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()

    @patch('services.client.chat.completions.create')
    def test_categorize_products_endpoint_error(self, mock_create):
        """Test product categorization endpoint with error response"""
        # Mock LLM service raising an exception
        mock_create.side_effect = Exception("API Error")
        
        payload = {
            "uncategorized_products": ["yogurt", "baguette", "milk"],
            "categorized_products": {"dairy": ["cheese"], "bakery": []}
        }
        response = self.client.post("/categorize-products", json=payload)
        
        # Verify error response
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Failed to categorize products")

    def test_invalid_request_body(self):
        """Test endpoint with invalid request body"""
        # Empty payload (missing required fields)
        payload = {}
        response = self.client.post("/recommendations", json=payload)
        
        # Verify validation error response
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)

# Allow running tests directly
if __name__ == "__main__":
    unittest.main()
