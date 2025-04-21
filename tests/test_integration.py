import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from main import app
import os
import pytest

# Skip all integration tests if GROQ_API_KEY is not set correctly
# This ensures tests don't fail in CI with invalid API keys
pytestmark = pytest.mark.skipif(
    os.environ.get("GROQ_API_KEY", "test_api_key") == "test_api_key" and os.environ.get("CI"),
    reason="Skipping integration tests in CI environment without valid API key"
)

# Set test API key for local testing
os.environ["GROQ_API_KEY"] = "test_api_key" 

class TestIntegration(unittest.TestCase):
    """Integration tests for the FastAPI application with mocked Groq API"""

    def setUp(self):
        """Setup method that runs before each test"""
        self.client = TestClient(app)

    @patch('services.client')
    def test_recommendations_integration(self, mock_client):
        """Integration test for recommendations endpoint"""
        # Setup mock client response
        mock_client.chat.completions.create.return_value = MagicMock(
            recommended_items=["queso rallado", "salsa de tomate", "aceite de oliva", "albahaca"]
        )
        
        # Make request to API
        payload = {"products": ["fideos", "ajo", "cebolla"]}
        response = self.client.post("/recommendations", json=payload)
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_items", data)
        self.assertEqual(len(data["recommended_items"]), 4)
        self.assertIn("queso rallado", data["recommended_items"])

    @patch('services.client')
    def test_dish_ingredients_integration(self, mock_client):
        """Integration test for dish ingredients endpoint"""
        # Setup mock client response
        mock_client.chat.completions.create.return_value = MagicMock(
            ingredients=["carne picada", "cebolla", "ajo", "tomate", "morrones", "aceite", "sal", "pimienta"]
        )
        
        # Make request to API
        response = self.client.get("/dishes/ingredients", params={"dish_name": "bolognesa"})
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ingredients", data)
        self.assertGreaterEqual(len(data["ingredients"]), 5)
        self.assertIn("carne picada", data["ingredients"])
        self.assertIn("tomate", data["ingredients"])

    @patch('services.client')
    def test_categorize_products_integration(self, mock_client):
        """Integration test for product categorization endpoint"""
        # Setup mock client response
        expected_categories = {
            "Lacteos": ["queso", "leche", "yogurt"],
            "Panaderia": ["pan", "facturas"]
        }
        mock_client.chat.completions.create.return_value = MagicMock(
            categories=expected_categories
        )
        
        # Make request to API
        payload = {
            "categorized_products": {"Lacteos": ["queso"], "Panaderia": ["pan"]},
            "uncategorized_products": ["leche", "yogurt", "facturas"]
        }
        response = self.client.post("/categorize-products", json=payload)
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("categories", data)
        self.assertIn("Lacteos", data["categories"])
        self.assertIn("Panaderia", data["categories"])
        self.assertIn("leche", data["categories"]["Lacteos"])
        self.assertIn("facturas", data["categories"]["Panaderia"])

    @patch('services.client')
    def test_error_handling_integration(self, mock_client):
        """Integration test for error handling"""
        # Setup mock client to raise exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        # Make request to API
        payload = {"products": ["fideos", "ajo", "cebolla"]}
        response = self.client.post("/recommendations", json=payload)
        
        # Assert error response
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Failed to get recommendations")

# Allow running tests directly
if __name__ == "__main__":
    unittest.main() 