# Movie-Recommender
Use of Collaborative Filtering where it takes the ratings of others on movies to match the user's highly rated movies and then recommends them.
This was made using Python and Flask!

# 🎬 Movie Recommender System

A collaborative filtering-based movie recommender web application built with **Python** and **Flask**. Users can register, rate movies, and receive personalized movie recommendations. The system uses **item-based collaborative filtering** to generate accurate suggestions based on user ratings and movie similarities.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask (`pip install flask`)
- WTForms (`pip install flask-wtf`)
- Other common libraries: `json`, `os`, `sqlite3`, etc.
- 
🔑 Key Features
User Authentication: Secure login and registration using WTForms

Dynamic Search: Search for movies by title, genre, or director while rating

Real-time Ratings: Ratings are stored and averaged dynamically

Collaborative Filtering: Recommendations use item-based similarity and intersection of raters

Performance Optimization:

Similarity matrix is cached to JSON

Recommendations are recalculated only when new ratings are submitted

🧠 Recommendation Algorithm
Uses Item-Based Collaborative Filtering:

Similarity Score Calculation:

For each movie rated by the user, compare it to all other movies.

Calculate cosine similarity using intersecting raters only.

Only store similarity scores > 0.7 (configurable).

Prediction:

For each unrated movie, multiply similarity scores with the user's ratings of similar movies.

Compute a weighted average for predicted rating.

Caching:

Similarity scores stored in similarity_matrix.json

User recommendations cached in saved/ to prevent redundant calculations

📊 Database Schema
users: Stores user credentials

movies: Movie metadata (title, director, genre)

movieRatings: Links user ID and movie ID with rating

✅ Usage Flow
Register/Login: Users must log in to access rating or recommendation features.

Rate Movies: Dynamic search and rate interface. Pre-fills if user has previously rated.

Get Recommendations:

Must rate some movies first

Up to 30 recommendations per page, sorted by predicted rating

💡 Customization Ideas
Increase movie pool beyond 100 titles

Adjust similarity score threshold

Add visualizations of user history or top movies

Improve search UX with autocomplete

👨‍💻 Author
Your Name
GitHub: @newbofcode
