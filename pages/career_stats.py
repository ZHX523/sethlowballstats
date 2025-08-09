import streamlit as st
import pandas as pd
import time
import functions
import main


st.set_page_config(layout="wide")



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

    functions.refresh_buttion()

    df, teams = functions.load_data()


player_options = df['Player'].unique().tolist()

selected_player = st.selectbox("***Select a Player***", player_options)

st.divider()

player_df = df[df['Player'] == selected_player]
fps = player_df['FPS'].mean().round(2)

player_profile = st.container()
player_profile.header(f'{selected_player}')
st.markdown(f":green-badge[:material/star: Avg Fantasy Value: {fps}] :orange-badge[⚠️ No Vision!] :gray-badge[Troll!]")




col1, col2, col3 = st.columns(3)

col_data = [
    (col1, ["Avg PTS", "Avg STL", "Avg FG %"]),
    (col2, ["Avg REB", "Avg BLK", "Avg 3P %"]),
    (col3, ["Avg AST", "Avg TO", "Avg TS %"])
]

for col, stats in col_data:
    with col:
        for stat in stats:
            stat_container = st.container(border=True)
            stat_container.write(stat)
            stat_container.write("PLACE HOLDER")


