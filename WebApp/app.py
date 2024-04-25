# importing required libraries
import streamlit as st
import pickle
import pandas as pd
import requests

# poster function fetched poster from tmdb database
def poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# recommend function recommends movies with their posters
def recommend(movie_name):
    movie_index = movie[movie['title_x'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list((enumerate(distances))), reverse=True, key=lambda x: x[1])[1:6]
    recommend_list = []
    recommend_poster = []
    for i in movie_list:
        movie_id = movie.iloc[i[0]].id
        recommend_list.append(movie.iloc[i[0]].title_x)
        recommend_poster.append(poster(movie_id))
    return recommend_list, recommend_poster


movie_dict = pickle.load(open('Movie_dict.pkl', 'rb'))  # loading pkl file from the notebook for movie directory
movie = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))  # loading pkl file from the notebook for similar movies

st.title('Movie Recommender System')  # set title of the webpage
selectMovie = st.selectbox("Which is your favorite movie?", movie['title_x'].values)  # creates a selection box

if st.button('Recommend'):  # create 5 area for recommended movie
    names, posters = recommend(selectMovie)
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
