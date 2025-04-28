import streamlit as st
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup


# 🔍 Function to fetch poster using Bing Image Search
def fetch_poster(movie_name):
    try:
        query = f"{movie_name} movie poster"
        url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}&form=HDRSC2"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.find_all("img")

        for img in image_elements:
            src = img.get("src")
            if src and src.startswith("http"):
                return src  # Return first valid image
        return "https://via.placeholder.com/300x450.png?text=No+Poster"
    except Exception as e:
        print(f"[Poster Error] {e}")
        return "https://via.placeholder.com/300x450.png?text=No+Poster"


# 📦 Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# 🤖 Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Top 5 excluding the selected one
        movie_name = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(fetch_poster(movie_name))

    return recommended_movie_names, recommended_movie_posters


# 🎬 Streamlit App UI
st.title('🎥 Movie Recommender System')

selected_movie_name = st.selectbox('Choose a movie:', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    st.subheader("🎯 Recommended Movies:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
