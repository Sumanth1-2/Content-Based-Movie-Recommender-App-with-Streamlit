# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:24:10 2024

@author: CB SUMANTH
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load the data
movies_data = pd.read_csv("C:/Users/CB SUMANTH/Downloads/tmdb_5000_movies.csv")
credits_data = pd.read_csv("C:/Users/CB SUMANTH/Downloads/tmdb_5000_credits.csv")

# Process the data
credits_data.columns = ['id', 'title', 'cast', 'crew']
data = movies_data.merge(credits_data, on="id")
data['overview'] = data['overview'].fillna('')

# Define a TF-IDF Vectorizer Object
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['overview'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a reverse map of indices and movie titles
movie_indices_map = pd.Series(data.index, index=data['title_x']).drop_duplicates()

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = movie_indices_map[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get the scores of the 10 most similar movies
        movie_indices = [i[0] for i in sim_scores]
        return data['title_x'].iloc[movie_indices].tolist()
    except KeyError:
        return []

# Streamlit app layout
st.title("Movie Recommendation System")
st.write("Enter a movie title to get recommendations based on the overview.")

# Movie input
movie_title = st.text_input("Movie Title:")

if movie_title:
    recommendations = get_recommendations(movie_title)
    if recommendations:
        st.write("### Recommended Movies:")
        for idx, title in enumerate(recommendations, start=1):
            st.write(f"{idx}. {title}")
    else:
        st.write("Movie not found. Please try another title.")

