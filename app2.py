# Fetch the neccesary python modules
import streamlit as st
import pickle
import pandas as pd
import requests


from scipy import spatial

def closest_movie(inp):
    data=movies.copy()
    inp_vector=model.encode(inp)
    s=data['embedding'].apply(lambda x: 1 - spatial.distance.cosine(x, inp_vector) )
    data=data.assign(similarity=s)
    return(data.sort_values('similarity',ascending=False).head(6))

def recommand_movie(movie):
    


    
    
    # Fetch the posters for each recommended movie
    recommended_movies =closest_movie(movie).original_title.to_list()
    recommended_movies_poster=[fetch_poster(i) for i in closest_movie(movie).id.to_list()]
    

    return recommended_movies,recommended_movies_poster

# Load the necessary python pickle files
#movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pickle.load(open('new_df_embeddings.pkl','rb'))

model = pickle.load(open('model_embedding.pkl','rb'))



# Fetch posters from the TMDb database
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Web app's hero section - Display Title, Dropdown
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
'Select a movie to recommend',
movies['original_title'].values)

# Output recommendations with posters
if st.button('Recommend'):
    name, posters = recommand_movie(selected_movie_name)
 
    col1, col2, col3, col4,  col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
