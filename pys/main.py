import streamlit as st
import pandas as pd
import numpy as np
import os


abs_path = os.path.abspath('')

csv = os.path.join(abs_path, "..", "resources", "books_1.Best_Books_Ever.csv")
df = pd.read_csv(csv)

# Initialization
if 'df_user_input' not in st.session_state:
    st.session_state['df_user_input'] = pd.DataFrame(columns=["title", "rating"])


st.set_page_config(page_title="Book recommender", page_icon="📖")

tab_vote, tab_recomendation = st.tabs(["Vote books","Recomendation"])

with tab_vote:


    book = st.selectbox('Select the book', options = df["title"].values)

    punctuation = st.slider("Select punctuation", 0, 10)

    vote = st.button("Vote",help="")

if vote:
    st.session_state['df_user_input'] = st.session_state['df_user_input'].append({"title": book, "rating":punctuation}, ignore_index = True)


st.write(st.session_state['df_user_input'])