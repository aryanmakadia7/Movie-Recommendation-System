import streamlit as st
import pickle
import pandas as pd

# Configure page metadata and layout
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ----------------- Load Data & Models ----------------- #
@st.cache_data
def load_data():
    # Load data using your repository's exact filenames
    movies_df = pickle.load(open('movie_data.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    return movies_df, similarity_matrix

# Execute the loader to assign movies and similarity
movies, similarity = load_data()

# ----------------- Recommendation Logic ----------------- #
def recommend(movie_title):
    # Locate index of the selected movie
    movie_index = movies[movies['title'] == movie_title].index[0]
    
    # Sort pairwise similarity scores in descending order
    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )
    
    # Extract the top 5 recommended movie titles (excluding the movie itself at index 0)
    recommended_titles = []
    for item in distances[1:6]:
        recommended_titles.append(movies.iloc[item[0]].title)
        
    return recommended_titles

# ----------------- Streamlit User Interface ----------------- #
st.title("🎬 Movie Recommender System")
st.write("Select a movie from the dropdown to get personalized recommendations.")

# Dropdown selection populated from your movie titles
selected_movie = st.selectbox(
    "Type or select a movie you like:",
    movies['title'].values
)

# Recommendation trigger button
if st.button("Show Recommendations"):
    recommendations = recommend(selected_movie)
    
    st.subheader("Top Recommendations for You:")
    cols = st.columns(5)
    for col, title in zip(cols, recommendations):
        with col:
            st.info(title)