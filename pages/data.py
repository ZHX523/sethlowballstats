import streamlit as st
import pandas as pd
import time
import functions
import main

st.set_page_config(layout="wide")

if "data_refreshed" not in st.session_state:
    st.session_state.data_refreshed = False


st.markdown("""
    <style>
    div.stButton > button[kind="secondary"] {
        background-color: #007bff;  /* Bootstrap Blue */
        color: white;
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    functions.home_button()
    functions.career_button()
    functions.leaderboard_button()
    functions.games_played_together()
    functions.refresh_buttion()


    df, teams = functions.load_data()
    st.divider()


