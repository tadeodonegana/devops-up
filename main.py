import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from schemas import (
    RecommendationRequest,
    RecommendationResponse,
    DishIngredientsResponse,
    CategorizationRequest,
    CategorizationResponse,
)
import services
import sentry_sdk
from sentry_sdk import logger as sentry_logger
sentry_sdk.init(
    dsn="https://45d96cc649186cfbb6feb39753ff005c@o4509340585099264.ingest.us.sentry.io/4509340587720704",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    _experiments={
        "enable_logs": True,
    }
)

app = FastAPI(
    title="Tote Backend API",
    description="A FastAPI backend for recommendations, dish ingredients, and product categorization using Groq's LLaMa 3.3 70B.",
    version="1.0.0",
)

# Enable CORS for public endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    sentry_logger.debug('Health check endpoint called')
    return {"status": "ok"}

@app.post("/recommendations", response_model=RecommendationResponse)
async def recommendations_endpoint(request: RecommendationRequest):
    try:
        sentry_logger.info('Processing recommendations request for {count} products', count=len(request.products))
        recommended_items = services.get_recommendations(request.products)
        sentry_logger.info('Successfully generated {count} recommendations', count=len(recommended_items))
        return RecommendationResponse(recommended_items=recommended_items)
    except Exception as e:
        sentry_logger.error('Failed to get recommendations: {error}', error=str(e))
        print("Error in recommendations_endpoint:", e)
        raise HTTPException(status_code=500, detail="Failed to get recommendations")

@app.get("/dishes/ingredients", response_model=DishIngredientsResponse)
async def dish_ingredients_endpoint(dish_name: str = Query(..., description="Name of the dish to get ingredients for")):
    try:
        sentry_logger.info('Fetching ingredients for dish: {dish}', dish=dish_name)
        ingredients = services.get_dish_ingredients(dish_name)
        sentry_logger.info('Found {count} ingredients for {dish}', count=len(ingredients), dish=dish_name)
        return DishIngredientsResponse(ingredients=ingredients)
    except Exception as e:
        sentry_logger.error('Failed to get ingredients for dish {dish}: {error}', dish=dish_name, error=str(e))
        print("Error in dish_ingredients_endpoint:", e)
        raise HTTPException(status_code=500, detail="Failed to get dish ingredients")

@app.post("/categorize-products", response_model=CategorizationResponse)
async def categorize_products_endpoint(request: CategorizationRequest):
    try:
        sentry_logger.info(
            'Categorizing {uncategorized_count} products based on {categorized_count} existing categorized products',
            uncategorized_count=len(request.uncategorized_products),
            categorized_count=len(request.categorized_products)
        )
        categorized = services.categorize_products(request.categorized_products, request.uncategorized_products)
        sentry_logger.info('Successfully categorized products into {category_count} categories', category_count=len(categorized))
        return CategorizationResponse(categories=categorized)
    except Exception as e:
        sentry_logger.error('Failed to categorize products: {error}', error=str(e))
        print("Error in categorize_products_endpoint:", e)
        raise HTTPException(status_code=500, detail="Failed to categorize products")

@app.get("/sentry-debug")
async def trigger_error():
    sentry_logger.warning('Debug endpoint called - about to trigger an error')
    division_by_zero = 1 / 0

# AWS Lambda handler
handler = Mangum(app)
