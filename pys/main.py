import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Book recommender", page_icon="📖")

tab_model, tab_mapas = st.tabs(["Vote books","Recomendatios"])

with tab_model:


    city = st.selectbox('Select your city', options = ["Madrid", "Barcelona", "London"])