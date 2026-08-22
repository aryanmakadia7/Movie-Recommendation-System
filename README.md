# 🎬 Movie Recommendation System

A machine learning based movie recommendation system built using Python.

The system recommends movies similar to a selected movie using
TF-IDF vectorization and cosine similarity.

## 🚀 Features

- 🎬 Select a movie
- 🔎 Search movies
- ⭐ View movie ratings
- 📅 View release dates
- 📝 View movie overview
- 🍿 Get top 5 similar movies
- 🎯 Display similarity percentage
- 🖥️ User-friendly Tkinter GUI

## 🧠 Machine Learning

The recommendation system uses:

- TF-IDF Vectorization
- Cosine Similarity
- Natural Language Processing techniques

Movie information such as genres, keywords, overview, tagline,
and original title are combined into a single 'tags' feature.

TF-IDF converts the text data into numerical vectors, and cosine
similarity is used to find movies with similar content.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Tkinter
- Pickle

## 📂 Project Structure

Movie-Recommendation-System/
│
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── train_model.py
├── app.py
├── movie_data.pkl
├── similarity.pkl
├── movie_indices.pkl
├── requirements.txt
├── README.md
└── .gitignore