import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import joblib

#API KEY HERE
API_KEY = "6bc60a1e582b40369aa8a66bd086be27"  # <--- CHANGE THIS
BASE_URL = "https://api.spoonacular.com/recipes"

print("🔄 Fetching recipes from Spoonacular...")

recipes = []
for i in range(0, 100, 10):
    response = requests.get(
        f"{BASE_URL}/complexSearch",
        params={
            "apiKey": API_KEY,
            "number": 10,
            "offset": i,
            "addRecipeInformation": True,
            "fillIngredients": True
        }
    )
    
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        break
        
    data = response.json()
    
    for recipe in data.get("results", []):
        ingredient_list = []
        for ing in recipe.get("extendedIngredients", []):
            ingredient_list.append(ing.get("name", "").lower())
        
        if ingredient_list:
            recipes.append({
                "title": recipe.get("title", "Unknown"),
                "ingredients": ingredient_list,
                "ingredients_text": " ".join(ingredient_list),
                "image": recipe.get("image", ""),
                "readyInMinutes": recipe.get("readyInMinutes", 30),
                "servings": recipe.get("servings", 2)
            })
    
    print(f"   Fetched {len(recipes)} recipes so far...")

print(f"✅ Found {len(recipes)} recipes with ingredients")

if len(recipes) == 0:
    print("❌ No recipes found! Check your API key.")
    exit()

df = pd.DataFrame(recipes)
vectorizer = CountVectorizer(stop_words="english", min_df=2, max_df=0.8)
ingredient_matrix = vectorizer.fit_transform(df["ingredients_text"])

joblib.dump(df, "recipe_data.joblib")
joblib.dump(ingredient_matrix, "ingredient_matrix.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")

print(f"✅ Saved {len(df)} recipes with {ingredient_matrix.shape[1]} unique ingredients")