import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load original dataset
movies = pd.read_csv('movies.csv')

# Basic preprocessing: combine useful fields
movies['tags'] = movies['overview'].fillna('') + " " + movies['genres'].fillna('')

# Optional: add cast, director, keywords if you have them

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Save the similarity matrix
similarity = cosine_similarity(vectors)
pickle.dump(similarity, open('similarity.pkl', 'wb'))

# Save updated movies.csv with tags
movies.to_csv('movies.csv', index=False)
