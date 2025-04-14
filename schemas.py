from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union

class RecommendationRequest(BaseModel):
    products: List[str]

class RecommendationResponse(BaseModel):
    recommended_items: List[str]

class DishIngredientsResponse(BaseModel):
    ingredients: List[str]

class CategorizationRequest(BaseModel):
    categorized_products: Dict[str, List[str]]  # Category name to list of products
    uncategorized_products: List[str]  # Products that need to be categorized

# For categorization, we can return any dict mapping category names to lists of strings.
class CategorizationResponse(BaseModel):
    categories: Dict[str, List[str]]
