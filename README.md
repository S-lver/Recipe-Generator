# 🍳 Smart Recipe Generator

A recipe recommendation engine that suggests recipes based on ingredients you already have at home.

## Features
- 🔍 Search recipes by ingredients
- 📊 Similarity scoring using NLP (CountVectorizer + Cosine Similarity)
- 🚀 FastAPI backend with auto-generated Swagger docs
- 🎨 Clean Bootstrap frontend
- 📦 Docker support

## Tech Stack
- **Backend:** FastAPI, Python
- **ML/NLP:** Scikit-learn (CountVectorizer, Cosine Similarity)
- **Data:** Spoonacular API
- **Frontend:** HTML, CSS, Bootstrap, Vanilla JS
- **Deployment:** Ready for Render.com + Netlify

## Installation

### 1. Clone the repository
\\\ash
git clone https://github.com/YOUR_USERNAME/smart-recipe-generator.git
cd smart-recipe-generator
\\\

### 2. Create and activate virtual environment
\\\ash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\\\

### 3. Install dependencies
\\\ash
pip install -r requirements.txt
\\\

### 4. Get Spoonacular API Key
1. Go to https://spoonacular.com/food-api
2. Sign up for a free account
3. Copy your API key

### 5. Run data preparation
\\\ash
python data_prep.py
\\\

### 6. Start the API server
\\\ash
uvicorn main:app --reload
\\\

### 7. Serve the frontend
\\\ash
cd frontend
python -m http.server 3000
\\\

### 8. Open in browser
- API: http://localhost:8000/docs
- Frontend: http://localhost:3000

## API Endpoints
- GET /health - Health check
- POST /recommend - Get recipe recommendations

### Example Request
\\\json
POST /recommend
{
    "ingredients": ["chicken", "rice", "garlic"],
    "top_n": 5
}
\\\

## Project Structure
\\\
smart-recipe-generator/
├── data_prep.py          # Data fetching and preprocessing
├── model.py              # Recommendation model
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── frontend/
│   └── index.html       # Frontend interface
└── README.md            # This file
\\\

## License
MIT

## Author
[Your Name]
