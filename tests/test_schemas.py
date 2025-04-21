import unittest
from pydantic import ValidationError

from schemas import (
    RecommendationRequest, 
    RecommendationResponse, 
    DishIngredientsResponse, 
    CategorizationRequest, 
    CategorizationResponse
)

class TestSchemas(unittest.TestCase):
    """Test class for Pydantic schema validation"""

    def test_recommendation_request_valid(self):
        """Test valid RecommendationRequest data"""
        data = {"products": ["pasta", "tomato sauce", "olive oil"]}
        request = RecommendationRequest(**data)
        self.assertEqual(request.products, data["products"])

    def test_recommendation_request_invalid(self):
        """Test invalid RecommendationRequest data"""
        data = {"products": "not a list"}  # Should be a list
        with self.assertRaises(ValidationError):
            RecommendationRequest(**data)

    def test_recommendation_response_valid(self):
        """Test valid RecommendationResponse data"""
        data = {"recommended_items": ["garlic", "basil", "parmesan", "black pepper"]}
        response = RecommendationResponse(**data)
        self.assertEqual(response.recommended_items, data["recommended_items"])

    def test_recommendation_response_invalid(self):
        """Test invalid RecommendationResponse data"""
        data = {"recommended_items": "not a list"}  # Should be a list
        with self.assertRaises(ValidationError):
            RecommendationResponse(**data)

    def test_dish_ingredients_response_valid(self):
        """Test valid DishIngredientsResponse data"""
        data = {"ingredients": ["flour", "eggs", "milk", "salt"]}
        response = DishIngredientsResponse(**data)
        self.assertEqual(response.ingredients, data["ingredients"])

    def test_dish_ingredients_response_invalid(self):
        """Test invalid DishIngredientsResponse data"""
        data = {"ingredients": "not a list"}  # Should be a list
        with self.assertRaises(ValidationError):
            DishIngredientsResponse(**data)

    def test_categorization_request_valid(self):
        """Test valid CategorizationRequest data"""
        data = {
            "categorized_products": {"dairy": ["cheese"], "produce": ["apple"]},
            "uncategorized_products": ["milk", "yogurt", "banana"]
        }
        request = CategorizationRequest(**data)
        self.assertEqual(request.categorized_products, data["categorized_products"])
        self.assertEqual(request.uncategorized_products, data["uncategorized_products"])

    def test_categorization_request_invalid_categorized(self):
        """Test invalid categorized_products in CategorizationRequest"""
        data = {
            "categorized_products": "not a dict",  # Should be a dict
            "uncategorized_products": ["milk", "yogurt", "banana"]
        }
        with self.assertRaises(ValidationError):
            CategorizationRequest(**data)

    def test_categorization_request_invalid_uncategorized(self):
        """Test invalid uncategorized_products in CategorizationRequest"""
        data = {
            "categorized_products": {"dairy": ["cheese"], "produce": ["apple"]},
            "uncategorized_products": "not a list"  # Should be a list
        }
        with self.assertRaises(ValidationError):
            CategorizationRequest(**data)

    def test_categorization_response_valid(self):
        """Test valid CategorizationResponse data"""
        data = {
            "categories": {
                "dairy": ["milk", "cheese", "yogurt"],
                "produce": ["apple", "banana"]
            }
        }
        response = CategorizationResponse(**data)
        self.assertEqual(response.categories, data["categories"])

    def test_categorization_response_invalid(self):
        """Test invalid CategorizationResponse data"""
        data = {"categories": "not a dict"}  # Should be a dict
        with self.assertRaises(ValidationError):
            CategorizationResponse(**data)

# Allow running tests directly
if __name__ == "__main__":
    unittest.main() 