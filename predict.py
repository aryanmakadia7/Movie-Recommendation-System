import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Load pickled datasets
@st.cache_data
def load_data():
    movies_df = pickle.load(open('movie_data.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    return movies_df, similarity_matrix

movies, similarity = load_data()

# Recommendation logic
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )
    
    recommended_titles = []
    for item in distances[1:6]:
        recommended_titles.append(movies.iloc[item[0]].title)
        
    return recommended_titles

# UI Layout
st.title("🎬 Movie Recommender System")
st.write("Select a movie from the dropdown to get personalized recommendations.")

selected_movie = st.selectbox(
    "Type or select a movie you like:",
    movies['title'].values
)

if st.button("Show Recommendations"):
    recommendations = recommend(selected_movie)
    
    st.subheader("Top Recommendations for You:")
    cols = st.columns(5)
    for col, title in zip(cols, recommendations):
        with col:
            st.info(title)