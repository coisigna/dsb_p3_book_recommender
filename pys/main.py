import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import random
from funcs import *


st.set_page_config(page_title="Book recommender", page_icon="📖")

clicked = False

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


st.title("Book Recommender")

st.subheader("**Vote some books to get the best recommendation**")


tab_vote, tab_recommendation = st.tabs(["Vote books","Recommendation"])

with tab_vote:

    sb_book = st.selectbox('Select the book', options = st.session_state['df_main']["title"].values, help="Write in the box to use it as an easy finder")

    sl_punctuation = st.slider("Select rating", 0, 10)

    bu_vote = st.button("Vote",help="")

    if bu_vote:

        st.session_state['df_user_input'] = st.session_state['df_user_input'].append({"title": sb_book, "rating":sl_punctuation}, ignore_index = True)
        st.session_state['df_user_input'].drop_duplicates(inplace=True)

        benefits = ["Regular reading has been linked to improved memory, concentration, and critical thinking skills.",
                    "Reading is a great way to learn about new topics and gain a deeper understanding of the world around you.",    
                    "Reading can help improve writing skills by exposing individuals to different styles and structures of written communication.",    
                    "Reading fiction and other forms of storytelling can help individuals develop empathy, emotional intelligence, and a better understanding of human nature.",    
                    "Reading can be a great way to relax and unwind, helping to reduce stress and improve overall mental well-being.",    
                    "Reading requires focus and concentration, which can help individuals improve these skills in other areas of their lives.",    
                    "Reading can inspire and stimulate the imagination, leading to increased creativity and innovation.",    
                    "Reading books from different cultures and backgrounds can broaden perspectives and deepen cultural awareness.",    
                    "Reading is a source of pleasure and can add to overall happiness and enjoyment of life.",    
                    "Reading before bed can help individuals relax and fall asleep more easily.",    
                    "Reading can help improve memory recall and retention.",    
                    "Increased vocabulary and comprehension: Regular reading can help individuals improve their vocabulary and comprehension skills.",    
                    "Reading can help to keep the mind sharp and active, leading to improved mental agility.",    
                    "Reading stimulates the imagination and can inspire creativity in individuals.",    
                    "Reading and learning about different perspectives can help individuals improve their problem-solving skills.",    
                    "Regular reading can help individuals improve their focus and attention span.",    
                    "Reading exposes individuals to new ideas and information, which can help them make more informed decisions.",    
                    "Reading books on communication and social skills can help individuals improve their interpersonal skills.",    
                    "Regular reading has been linked to a number of health benefits, including reduced stress levels and improved mental well-being."]

        i = random.randint(0,len(benefits)-1)
        st.success(benefits[i])

    st.table(data=st.session_state['df_user_input'])

    bu_gen_recom = st.button("Generate my recommendation!")


if bu_gen_recom:

    with tab_vote:
        st.success("Success!! Your recommendatión is ready, go to the next tab to check it!")

   
    st.balloons()

    df_ui, df_weighted_genre_matrix = create_weighted_genre_matrix(df_ui = st.session_state['df_user_input'], df_main = st.session_state['df_main'])

    df_weighted_books_matrix = create_weighted_books_matrix(df_weighted_genre_matrix = df_weighted_genre_matrix, df_ui = df_ui)

    df_recommendation = create_recommendation_dataframe(df_start=st.session_state['df_cleansed'], df_weighted_books_matrix = df_weighted_books_matrix)

    with tab_recommendation:

        img_book_1, stuff_book_1 = st.columns(2)

        with img_book_1:

            st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[0]})")   

        with stuff_book_1:

            st.write(df_recommendation["title"].iat[0])
            st.write(df_recommendation["description"].iat[0])
            st.write(f"ISBN: {df_recommendation['isbn'].iat[0]}")
            st.write(f"Rating: {str(df_recommendation['rating'].iat[0])}")

        stuff_book_2, img_book_2 = st.columns(2)

        with img_book_2:

            st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[1]})")   

        with stuff_book_2:

            st.write(df_recommendation["title"].iat[1])
            st.write(df_recommendation["description"].iat[1])
            st.write(f"ISBN: {df_recommendation['isbn'].iat[1]}")
            st.write(f"Rating: {str(df_recommendation['rating'].iat[1])}")

        img_book_3, stuff_book_3 = st.columns(2)

        with img_book_3:

            st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[2]})")   

        with stuff_book_3:

            st.write(df_recommendation["title"].iat[2])
            st.write(df_recommendation["description"].iat[2])
            st.write(f"ISBN: {df_recommendation['isbn'].iat[2]}")
            st.write(f"Rating: {str(df_recommendation['rating'].iat[2])}")

        stuff_book_4, img_book_4 = st.columns(2)

        with img_book_4:

            st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[3]})")   

        with stuff_book_4:

            st.write(df_recommendation["title"].iat[3])
            st.write(df_recommendation["description"].iat[3])
            st.write(f"ISBN: {df_recommendation['isbn'].iat[3]}")
            st.write(f"Rating: {str(df_recommendation['rating'].iat[3])}")

        img_book_5, stuff_book_5 = st.columns(2)

        with img_book_5:

            st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[4]})")   

        with stuff_book_5:

            st.write(df_recommendation["title"].iat[4])
            st.write(df_recommendation["description"].iat[4])
            st.write(f"ISBN: {df_recommendation['isbn'].iat[4]}")
            st.write(f"Rating: {str(df_recommendation['rating'].iat[4])}")




