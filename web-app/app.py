import os
import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')

movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_list[movies_list['title'] ==  movie].index[0]
    distances = similarity[movie_index]
    sorted_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in sorted_movies:
        movie_id = movies_list.iloc[i[0]].movie_id

        recommend_movies.append(movies_list.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

movies = movies_list['title'].values

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])