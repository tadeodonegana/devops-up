import os
import json
from groq import Groq
import instructor
from typing import List, Dict

# Import Pydantic models
from schemas import RecommendationResponse, DishIngredientsResponse, CategorizationResponse

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Only initialize the Groq client if API key is available
# This helps with testing environments
if GROQ_API_KEY and GROQ_API_KEY != "test_api_key":
    # Initialize the Groq client
    client = Groq(api_key=GROQ_API_KEY)
    # Enable instructor patches for Groq client
    client = instructor.from_groq(client)
else:
    # For testing environments, create a placeholder
    client = None

def get_recommendations(products: List[str]) -> List[str]:
    """Get shopping recommendations based on a list of products."""
    prompt = f"""
    You are an expert assistant who recommends complementary products for shopping lists in Argentina.
    Your task is to suggest products that go well with the most recently added products. Especially for preparing meals.

    ### Instructions:
    1. Analyze each of the last 3 products added: {', '.join(products[:3] if len(products) >= 3 else products)}
    2. For each recent product, recommend exactly 4 complementary products typically purchased together in Argentina
    3. Do not recommend products already in the current list: {', '.join(products)}
    4. Consider the complete context of the list to make coherent recommendations
    5. Prioritize products that complement multiple items on the list when possible

    ### Examples:

    #### Example 1:
    Current shopping list: ["leche", "pan", "ajo", "cebolla", "fideos"]
    Recently added products: ["ajo", "cebolla", "fideos"]
    Recommendations: ["salsa de tomate", "queso rallado", "aceite de oliva", "albahaca", "vino tinto"]

    #### Example 2:
    Current shopping list: ["manteca", "pan lactal", "azúcar", "café"]
    Recently added products: ["pan lactal", "azúcar", "café"]
    Recommendations: ["dulce de leche", "mermelada", "medialunas", "yogur", "frutas para el desayuno"]

    #### Example 3:
    Current shopping list: ["limón", "carne", "carbón", "sal gruesa"]
    Recently added products: ["carne", "carbón", "sal gruesa"]
    Recommendations: ["chimichurri", "chorizo", "morcilla", "ensalada", "pan", "fernet"]

    #### Example 4:
    Current shopping list: ["arroz", "pollo", "tomate", "cebolla", "lechuga", "zanahoria", "pepino"]
    Recently added products: ["lechuga", "zanahoria", "pepino"]
    Recommendations: ["aceite de oliva", "vinagre", "limón", "rúcula", "aderezo para ensalada"]

    #### Example 5:
    Current shopping list: ["leche", "manteca", "harina", "azúcar", "huevos"]
    Recently added products: ["harina", "azúcar", "huevos"]
    Recommendations: ["polvo para hornear", "esencia de vainilla", "chocolate", "dulce de leche", "crema"]
    
    ### Context
    Current shopping list: {', '.join(products)}
    Recently added products: {', '.join(products[:3] if len(products) >= 3 else products)}
    """
    
    print("Calling Groq API for recommendations with prompt:", prompt)
    
    # For testing environments, return mock data if no client
    if client is None:
        print("Using mock data for testing environment")
        return ["salsa de tomate", "queso rallado", "aceite de oliva", "albahaca"]
        
    # Use instructor with the Pydantic model to get structured response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=RecommendationResponse,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.recommended_items

def get_dish_ingredients(dish_name: str) -> List[str]:
    """Get ingredients needed for a specific dish."""
    prompt = f"""
    List the ingredients needed to make {dish_name}. Answer in spanish. Do not output the name of the dish. The user is from Argentina, so take in consideration that they might not have access to certain products.
    """
    print("Calling Groq API for dish ingredients with prompt:", prompt)
    
    # For testing environments, return mock data if no client
    if client is None:
        print("Using mock data for testing environment")
        return ["carne picada", "cebolla", "ajo", "tomate", "morrones", "aceite", "sal", "pimienta"]
    
    # Use instructor with the Pydantic model to get structured response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=DishIngredientsResponse,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.ingredients

def categorize_products(categorized_products: Dict[str, List[str]], uncategorized_products: List[str]) -> Dict[str, List[str]]:
    """Categorize products into appropriate categories."""
    prompt = f"""
    I have the following products already categorized:
    {json.dumps(categorized_products, indent=2)}
    
    Please categorize these additional products into appropriate categories:
    {', '.join(uncategorized_products)}
    
    Available categories:
        - Panaderia
        - Lacteos
        - Carniceria
        - Fiambres y embutidos
        - Frutas y verduras
        - Almacen
        - Bebidas
        - Congelados
        - Rotiseria
        - Limpieza
        - Perfumeria e higiene personal
        - Mascotas
        - Bazar y hogar
        - Ferreteria
        - Papeleria y libreria
        - Textil y vestimenta
        - Otros
    
    The categories should be the available categories listed above.
    If you can't categorize a product, just return it in the "Otros" category.
    Answer in spanish. The user is from Argentina, so take in consideration that they might not have access to certain products.
    """
    print("Calling Groq API for product categorization with prompt:", prompt)
    
    # For testing environments, return mock data if no client
    if client is None:
        print("Using mock data for testing environment")
        return {
            "Lacteos": ["queso", "leche", "yogurt"],
            "Panaderia": ["pan", "facturas"]
        }
    
    # Use instructor with the Pydantic model to get structured response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=CategorizationResponse,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.categories