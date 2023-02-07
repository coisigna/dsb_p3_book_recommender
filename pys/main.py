import streamlit as st
import pandas as pd
import numpy as np
import os
from my_funcs import *

st.set_page_config(page_title="Book recommender", page_icon="📖")

abs_path = os.path.dirname(os.path.abspath(__file__))
csv = os.path.join(abs_path, "..", "resources", "books_1.Best_Books_Ever.csv")

if 'df_cleansed' not in st.session_state:

    st.session_state['df_cleansed'] = data_cleanse(csv)

if 'df_with_genres' not in st.session_state:
    
    st.session_state['df_with_genres'] = genres_to_cols(st.session_state['df_cleansed'])

if 'df_main' not in st.session_state:
    
    st.session_state['df_main'] = pages_to_cols(st.session_state['df_cleansed'],st.session_state['df_with_genres'])

if 'df_user_input' not in st.session_state:
    st.session_state['df_user_input'] = pd.DataFrame(columns=["title", "rating"])


tab_vote, tab_recomendation = st.tabs(["Vote books","Recomendation"])

with tab_vote:

    sb_book = st.selectbox('Select the book', options = st.session_state['df_main']["title"].values)

    sl_punctuation = st.slider("Select punctuation", 0, 10)

    bu_vote = st.button("Vote",help="")

if bu_vote:

    st.session_state['df_user_input'] = st.session_state['df_user_input'].append({"title": sb_book, "rating":sl_punctuation}, ignore_index = True)

st.dataframe(data=st.session_state['df_user_input'], width = 1500, height = 300)

bu_gen_recom = st.button("Generate my recommendation!")

if bu_gen_recom:

    df_ui, df_weighted_genre_matrix = create_weighted_genre_matrix(df_ui = st.session_state['df_user_input'], df_main = st.session_state['df_main'])

    st.write(df_ui)
    
    df_weighted_books_matrix = create_weighted_books_matrix(df_ui)

    df_recommendation = create_recommendation_dataframe(df_start=st.session_state['df_main'], df_weighted_books_matrix = df_weighted_books_matrix)

    st.dataframe(data = df_recommendation, width = 1500, height = 300)                                                        
