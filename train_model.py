import pandas as pd
import ast
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD THE MOVIE DATASET
# ============================================================

print("Loading movie dataset...")

movies = pd.read_csv(
    "data/tmdb_5000_movies.csv",
    encoding="latin1"
)

print("Movie dataset loaded successfully!")
print("Original Shape:", movies.shape)


# ============================================================
# 2. SELECT USEFUL COLUMNS
# ============================================================

# We only need these columns for our recommendation system.
# The credits dataset is not required for this version.

required_columns = [
    "id",
    "title",
    "genres",
    "keywords",
    "overview",
    "tagline",
    "original_title",
    "vote_average",
    "release_date"
]

movies = movies[required_columns].copy()


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

print("\nChecking missing values:")

print(movies.isnull().sum())

# Replace missing text values with empty strings
text_columns = [
    "genres",
    "keywords",
    "overview",
    "tagline",
    "original_title"
]

for column in text_columns:
    movies[column] = movies[column].fillna("")

# Replace missing ratings with 0
movies["vote_average"] = movies["vote_average"].fillna(0)

# Replace missing release dates
movies["release_date"] = movies["release_date"].fillna("")


# ============================================================
# 4. CONVERT JSON-LIKE DATA INTO TEXT
# ============================================================

def convert_to_text(value):
    """
    Converts columns such as genres and keywords from
    JSON-like strings into simple text.

    Example:

    [{"id": 28, "name": "Action"},
     {"id": 12, "name": "Adventure"}]

    becomes:

    Action Adventure
    """

    try:
        data = ast.literal_eval(value)

        if isinstance(data, list):

            names = []

            for item in data:

                if isinstance(item, dict) and "name" in item:
                    names.append(item["name"])

            return " ".join(names)

        return str(value)

    except:
        return str(value)


print("\nConverting genres and keywords...")

movies["genres"] = movies["genres"].apply(convert_to_text)

movies["keywords"] = movies["keywords"].apply(convert_to_text)


# ============================================================
# 5. CREATE THE TAGS COLUMN
# ============================================================

print("Creating movie tags...")

movies["tags"] = (
    movies["genres"] + " "
    + movies["keywords"] + " "
    + movies["overview"] + " "
    + movies["tagline"] + " "
    + movies["original_title"]
)


# Convert everything to lowercase
movies["tags"] = movies["tags"].str.lower()


# ============================================================
# 6. REMOVE DUPLICATE MOVIES
# ============================================================

movies = movies.drop_duplicates(subset="title")

print("\nShape after removing duplicates:")
print(movies.shape)


# ============================================================
# 7. CREATE TF-IDF VECTORS
# ============================================================

print("\nCreating TF-IDF vectors...")

tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(movies["tags"])

print("TF-IDF matrix created!")
print("TF-IDF Shape:", tfidf_matrix.shape)


# ============================================================
# 8. CALCULATE COSINE SIMILARITY
# ============================================================

print("\nCalculating cosine similarity...")

similarity = cosine_similarity(tfidf_matrix)

print("Cosine similarity calculated!")
print("Similarity Matrix Shape:", similarity.shape)


# ============================================================
# 9. CREATE MOVIE INDEX
# ============================================================

movies = movies.reset_index(drop=True)

movie_indices = pd.Series(
    movies.index,
    index=movies["title"].str.lower()
).drop_duplicates()


# ============================================================
# 10. RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie_name, number_of_recommendations=5):

    movie_name = movie_name.lower().strip()

    # Check whether movie exists
    if movie_name not in movie_indices:
        print("\nMovie not found!")

        # Show some movies that are available
        print("\nExample movies available in the dataset:")

        for title in movies["title"].head(10):
            print("-", title)

        return []

    # Get movie index
    index = movie_indices[movie_name]

    # Get similarity scores
    similarity_scores = list(enumerate(similarity[index]))

    # Sort from highest similarity to lowest
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    # Skip the first movie because it is the movie itself
    for i, score in similarity_scores[1:number_of_recommendations + 1]:

        recommendations.append({
            "title": movies.iloc[i]["title"],
            "similarity": round(score * 100, 2),
            "rating": movies.iloc[i]["vote_average"],
            "release_date": movies.iloc[i]["release_date"]
        })

    return recommendations


# ============================================================
# 11. TEST THE RECOMMENDATION SYSTEM
# ============================================================

print("\n" + "=" * 60)
print("TESTING MOVIE RECOMMENDATION SYSTEM")
print("=" * 60)

test_movie = "Interstellar"

recommendations = recommend(
    test_movie,
    number_of_recommendations=5
)

if recommendations:

    print(f"\nRecommendations for: {test_movie}")

    for number, movie in enumerate(recommendations, start=1):

        print(
            f"{number}. {movie['title']} "
            f"| Similarity: {movie['similarity']}% "
            f"| Rating: {movie['rating']}"
        )


# ============================================================
# 12. SAVE THE MODEL
# ============================================================

print("\nSaving model files...")

# Save movie information
with open("movie_data.pkl", "wb") as file:
    pickle.dump(movies, file)

# Save similarity matrix
with open("similarity.pkl", "wb") as file:
    pickle.dump(similarity, file)

# Save movie index
with open("movie_indices.pkl", "wb") as file:
    pickle.dump(movie_indices, file)


print("\n" + "=" * 60)
print("MODEL CREATED SUCCESSFULLY!")
print("=" * 60)

print("\nCreated files:")
print("1. movie_data.pkl")
print("2. similarity.pkl")
print("3. movie_indices.pkl")

print("\nMovie Recommendation System is ready!")