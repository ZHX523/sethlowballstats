import streamlit as st
import pandas as pd
import time
import functions


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

    functions.refresh_buttion()


    df, teams = functions.load_data()

    st.divider()


    st.subheader('Pick a Game')

    team_options = df['Date'].unique()
    selected_date = st.sidebar.selectbox("Date", team_options)

    game_options = df[df['Date'] == selected_date]['Game'].unique()
    selected_game = st.sidebar.selectbox("Select a Game", game_options)

    game_id = df[(df['Date'] == selected_date) & (df['Game'] == selected_game)]





row1 = st.columns(1)

for col in row1:
    tile = col.container()
    tile.header(f'{selected_game} on {selected_date}')
    try:
        st.video(game_id.iloc[0]['Video URL'])
    except Exception as e:
        st.error(f"Data incomplete, fix underlying data!")


for team in teams:
    with st.container():

        table_html, team_score = functions.build_table_html(df,team,selected_date,selected_game)

        st.subheader(f'Team: {team} | **{team_score}** PTS', divider=True)
        st.caption(f'Fantasy Scoring: PTS = 1.2 | REB = 1 | AST = 1.5 | STL = 3 | BLK = 3 | TO = (-2)')

        st.markdown(table_html,unsafe_allow_html=True)






