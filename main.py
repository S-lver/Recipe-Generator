from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
import numpy as np
from model import RecipeRecommender

app = FastAPI(
    title="Smart Recipe Generator API",
    description="Find recipes based on ingredients you already have",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = RecipeRecommender()

class IngredientRequest(BaseModel):
    ingredients: List[str]
    top_n: int = 5

def convert_numpy_types(obj):
    """Convert NumPy types to Python native types"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

@app.get("/")
def root():
    return {"message": "🍳 Smart Recipe Generator API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "ok", "recipes_loaded": int(len(recommender.df))}

@app.post("/recommend")
def get_recommendations(request: IngredientRequest):
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="Please provide at least one ingredient")
    
    try:
        results = recommender.recommend(request.ingredients, top_n=request.top_n)
        
        if not results:
            return {
                "message": "No recipes found. Try more common ingredients.",
                "results": []
            }
        
        # Convert any NumPy types to Python native types
        results = convert_numpy_types(results)
        
        return {
            "message": f"Found {len(results)} recipes!",
            "input_ingredients": request.ingredients,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))