# 🎬 Movie Recommendation System

A simple **content-based movie recommendation system** built using Python and Flask. This project suggests similar movies based on a selected title using cosine similarity over combined tags like genres and overviews. Posters are dynamically fetched from the TMDB API.

---

## 🔍 Features

- Recommends 5 similar movies based on content similarity
- Uses `CountVectorizer` + Cosine Similarity
- TMDB API integration for fetching movie posters
- Prioritizes newer movies (post-2010), but backfills with older ones
- Built with a simple web UI using Flask and HTML/CSS

---

## 🚀 Tech Stack

- Python
- Flask
- Pandas
- Scikit-learn
- CountVectorizer
- TMDB API
- HTML/CSS

---

## 📂 Project Structure

│
├── app.py # Flask application file
├── similarity.py # Script to generate similarity.pkl
├── similarity.pkl # Precomputed similarity matrix (via Drive)
├── movies.csv # Dataset of movies with overview & genre
├── style.css # CSS file for styling
├── templates/
│ └── index.html # Flask template for homepage

---

## 🧠 How it Works

1. Takes a movie title input from the user.
2. Matches it with available titles in the dataset.
3. Computes cosine similarity from vectorized tags.
4. Recommends top 5 movies based on content similarity.
5. Displays movie posters using the TMDB API.

---

## 📥 How to Run

1. Clone the repository:
   ```bash
 git clone https://github.com/Shubham1919284/Movie-Recommendation-System-Static-.git
cd Movie-Recommendation-System-Static-
   
Install dependencies:

pip install -r requirements.txt
If similarity.pkl is not available:
Run : 
python similarity.py

----

Start the Flask app:
python app.py

----

Open your browser and go to http://127.0.0.1:5000
--> Now you are good to go and use it...........

-----------

## 👨‍💻 Author

**Shubham Kumar Jha**  
BTech CSE (Data Science) | Gulzar Group of Institutes (PTU)  
📧 Email: sk1919284@gmail.com | 🔗 LinkedIn: linkedin.com/in/shubham-kumar-jha-1a2b3c

