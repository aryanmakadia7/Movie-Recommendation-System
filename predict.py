import streamlit as st
import pickle
import pandas as pd
import requests

# Set page title and layout
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ----------------- Helper Functions ----------------- #
def fetch_poster(movie_id):
    """
    Optional: Fetch movie poster using TMDB API.
    If you don't use poster images, you can omit this function.
    """
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_TMDB_API_KEY&language=en-US"
        data = requests.get(url).json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    """
    Core recommendation logic (same as your Tkinter script).
    """
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        # Fetch movie details
        movie_id = movies.iloc[i[0]].movie_id if 'movie_id' in movies.columns else None
        recommended_movie_names.append(movies.iloc[i[0]].title)
        
        # If using posters:
        if movie_id:
            recommended_movie_posters.append(fetch_poster(movie_id))
   # 1. Define the caching loader function
@st.cache_data
def load_data():
    movies_df = pickle.load(open('movie_data.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    return movies_df, similarity_matrix

# 2. CALL THE FUNCTION to create the 'movies' variable:
movies, similarity = load_data()

# 3. Now you can use movies['title'].values safely:
st.title("🎬 Movie Recommender System")
st.write("Select a movie from the dropdown to get personalized recommendations.")

selected_movie = st.selectbox(
    "Type or select a movie you like:",
    movies['title'].values
)         
    return recommended_movie_names, recommended_movie_posters

# ----------------- Load Data / Models ----------------- #


# Button (replaces tk.Button)
if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)
    
    # Display results in 5 columns
    cols = st.columns(5)
    for col, name in zip(cols, names):
        with col:
            st.text(name)
            # If displaying posters:
            # st.image(poster)