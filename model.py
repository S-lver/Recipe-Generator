import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecipeRecommender:
    def __init__(self):
        self.df = joblib.load("recipe_data.joblib")
        self.matrix = joblib.load("ingredient_matrix.joblib")
        self.vectorizer = joblib.load("vectorizer.joblib")
    
    def recommend(self, user_ingredients, top_n=5):
        clean_input = " ".join([ing.lower().strip() for ing in user_ingredients])
        input_vector = self.vectorizer.transform([clean_input])
        similarities = cosine_similarity(input_vector, self.matrix).flatten()
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        top_indices = [i for i in top_indices if similarities[i] > 0]
        
        results = []
        for idx in top_indices:
            recipe = self.df.iloc[idx]
            
            # Convert NumPy types to Python native types
            similarity_score = float(similarities[idx])  # Convert to Python float
            ready_minutes = int(recipe.get("readyInMinutes", 30))  # Convert to Python int
            servings = int(recipe.get("servings", 2))  # Convert to Python int
            
            # Get ingredients as a list (convert if it's a NumPy array)
            ingredients = recipe["ingredients"]
            if hasattr(ingredients, 'tolist'):
                ingredients = ingredients.tolist()
            elif isinstance(ingredients, np.ndarray):
                ingredients = ingredients.tolist()
            else:
                ingredients = list(ingredients)  # Ensure it's a list
            
            results.append({
                "title": str(recipe["title"]),  # Convert to string
                "ingredients": ingredients,
                "image": str(recipe.get("image", "")),  # Convert to string
                "readyInMinutes": ready_minutes,
                "servings": servings,
                "similarity_score": round(similarity_score, 3)
            })
        
        return results

if __name__ == "__main__":
    recommender = RecipeRecommender()
    results = recommender.recommend(["chicken", "rice", "garlic"])
    for r in results:
        print(f"🍽️ {r['title']} (Score: {r['similarity_score']})")