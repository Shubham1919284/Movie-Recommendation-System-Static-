from flask import Flask, render_template, request
import pandas as pd
import pickle
import requests
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

TMDB_API_KEY = "220ae607aba8a49a9fe7e3e9707ac0d1"

# Load movies and similarity data
movies = pd.read_csv('movies.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Load vectorizer and fit_transform if needed
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags'].fillna('')).toarray()

def fetch_poster(movie_title):
    try:
        from requests.utils import quote
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={quote(movie_title)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'results' in data and data['results']:
            for result in data['results']:
                poster_path = result.get('poster_path')
                if poster_path:
                    return "https://image.tmdb.org/t/p/w500" + poster_path
        return "https://via.placeholder.com/300x450?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

def fetch_movie_tags_from_tmdb(movie_title):
    import httpx
    from urllib.parse import quote
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={quote(movie_title)}"
        r = httpx.get(url, timeout=10)
        data = r.json()
        if data["results"]:
            movie_id = data["results"][0]["id"]
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
            d = httpx.get(details_url).json()
            genres = " ".join([g["name"] for g in d.get("genres", [])])
            overview = d.get("overview", "")
            cast = " ".join([c["name"] for c in d.get("credits", {}).get("cast", [])[:5]])
            return genres + " " + overview + " " + cast
        return None
    except:
        return None

def recommend(movie):
    movie = movie.lower()

    # Step 1: Find closest match from titles
    matched_titles = movies[movies['title'].str.lower().str.contains(movie)]
    if matched_titles.empty:
        return [("Movie not found", "https://via.placeholder.com/300x450?text=Not+Found")]

    # Use the most relevant match (top one)
    idx = matched_titles.index[0]

    # Step 2: Compute similarity scores
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, reverse=True, key=lambda x: x[1])

    # Step 3: Filter top movies with preference for newer releases
    recommended = []
    count = 0

    for i in sorted_movies:
        title = movies.iloc[i[0]].title
        year = movies.iloc[i[0]].get("year", 2000)

        if year >= 2010 and title.lower() != movie:
            poster = fetch_poster(title)
            recommended.append((title, poster))
            count += 1
        if count == 5:
            break

    # Step 4: Fill with older ones if needed
    if count < 5:
        for i in sorted_movies:
            title = movies.iloc[i[0]].title
            if not any(title == t for t, _ in recommended):
                poster = fetch_poster(title)
                recommended.append((title, poster))
                if len(recommended) == 5:
                    break

    return recommended



@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    movie_name = None
    if request.method == 'POST':
        movie_name = request.form['movie']
        recommendations = recommend(movie_name)
    return render_template('index.html', recommendations=recommendations, movie_name=movie_name)

if __name__ == '__main__':
    app.run(debug=True)
