import unittest
from unittest.mock import patch, MagicMock

import services
from schemas import RecommendationResponse, DishIngredientsResponse, CategorizationResponse

class TestServices(unittest.TestCase):
    """Test class for service module functions"""

    @patch('services.client.chat.completions.create')
    def test_get_recommendations(self, mock_create):
        """Test get_recommendations service function"""
        # Mock the LLM response
        expected_items = ["queso rallado", "salsa de tomate", "aceite de oliva", "albahaca"]
        mock_create.return_value = MagicMock(recommended_items=expected_items)
        
        # Call the service function
        products = ["fideos", "ajo", "cebolla"]
        result = services.get_recommendations(products)
        
        # Verify result
        self.assertEqual(result, expected_items)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()
        # Extract call arguments
        call_args = mock_create.call_args[1]
        self.assertEqual(call_args["model"], "llama-3.3-70b-versatile")
        self.assertEqual(call_args["response_model"], RecommendationResponse)
        
    @patch('services.client.chat.completions.create')
    def test_get_dish_ingredients(self, mock_create):
        """Test get_dish_ingredients service function"""
        # Mock the LLM response
        expected_ingredients = ["carne picada", "cebolla", "ajo", "tomate", "morrones", "aceite", "sal", "pimienta"]
        mock_create.return_value = MagicMock(ingredients=expected_ingredients)
        
        # Call the service function
        dish_name = "bolognesa"
        result = services.get_dish_ingredients(dish_name)
        
        # Verify result
        self.assertEqual(result, expected_ingredients)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()
        # Extract call arguments
        call_args = mock_create.call_args[1]
        self.assertEqual(call_args["model"], "llama-3.3-70b-versatile")
        self.assertEqual(call_args["response_model"], DishIngredientsResponse)

    @patch('services.client.chat.completions.create')
    def test_categorize_products(self, mock_create):
        """Test categorize_products service function"""
        # Mock the LLM response
        expected_categories = {
            "Lacteos": ["queso", "leche", "yogurt"],
            "Panaderia": ["pan", "facturas"]
        }
        mock_create.return_value = MagicMock(categories=expected_categories)
        
        # Call the service function
        categorized = {"Lacteos": ["queso"], "Panaderia": ["pan"]}
        uncategorized = ["leche", "yogurt", "facturas"]
        result = services.categorize_products(categorized, uncategorized)
        
        # Verify result
        self.assertEqual(result, expected_categories)
        
        # Verify mock was called correctly
        mock_create.assert_called_once()
        # Extract call arguments
        call_args = mock_create.call_args[1]
        self.assertEqual(call_args["model"], "llama-3.3-70b-versatile")
        self.assertEqual(call_args["response_model"], CategorizationResponse)

# Allow running tests directly
if __name__ == "__main__":
    unittest.main() 