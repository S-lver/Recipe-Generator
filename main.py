from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

app = FastAPI(
    title="Smart Recipe Generator API",
    description="Find recipes based on ingredients you already have",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy load the recommender
recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        # Check if data files exist
        if not os.path.exists("recipe_data.joblib"):
            raise HTTPException(
                status_code=503,
                detail="Recipe data not ready. Please try again in a moment."
            )
        try:
            from model import RecipeRecommender
            recommender = RecipeRecommender()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load recommendation model: {str(e)}"
            )
    return recommender

class IngredientRequest(BaseModel):
    ingredients: List[str]
    top_n: int = 5

@app.get("/")
def root():
    return {"message": "🍳 Smart Recipe Generator API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    data_ready = os.path.exists("recipe_data.joblib")
    return {
        "status": "ok", 
        "recipes_loaded": "unknown" if not data_ready else "loaded",
        "data_ready": data_ready
    }

@app.post("/recommend")
def get_recommendations(request: IngredientRequest):
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="Please provide at least one ingredient")
    
    try:
        recommender = get_recommender()
        results = recommender.recommend(request.ingredients, top_n=request.top_n)
        
        if not results:
            return {
                "message": "No recipes found. Try more common ingredients.",
                "results": []
            }
        
        return {
            "message": f"Found {len(results)} recipes!",
            "input_ingredients": request.ingredients,
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
