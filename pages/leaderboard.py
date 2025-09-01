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


functions.load_data()
players = df['Player'].unique().tolist()

player_avg = df.groupby('Player', as_index=False)[df.select_dtypes(include='number').columns].mean()

player_avg = player_avg.sort_values(by="FPS",ascending=False).reset_index(drop=True)
player_avg = player_avg.round(2)

games_per_player = df.groupby("Player").size()
valid_players = games_per_player[games_per_player >= 15].index
player_avg_filtered = player_avg[player_avg['Player'].isin(valid_players)]


col1, col2 = st.columns(2)

with col1:
    main_container = st.container(border=False)
    main_container.header("👑  Leaderboard (min. 15 Games)")


    for count, row in enumerate(player_avg_filtered.itertuples(index=False), start=1):

        games_played = df[df["Player"] == row.Player].shape[0]

        crown = " 👑" if count == 1 else ""
        tile = main_container.container(border=True)
        tile.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center;font-weight: bold; font-size: 20px;">
                <div>{count}. {crown} {row.Player}</div>
                <div>FPS: {row.FPS:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        tile.caption(f'Games Played: **{games_played}** ')


with col2:
    second_container = st.container(border=False)
    second_container.header("🏆  Seth Low NBA Awards")


    functions.awards_tile('MVP 👑',
                          player_avg_filtered.loc[player_avg_filtered['FPS'].idxmax(), 'Player'],
                          player_avg_filtered['FPS'].max()
                          ,'FPS')


    functions.awards_tile("Point God",
                          player_avg_filtered.loc[player_avg_filtered['AST'].idxmax(), 'Player'],
                          player_avg_filtered['AST'].max(),
                          "AST")

    functions.awards_tile("Turnover King",
                          player_avg_filtered.loc[player_avg_filtered['TO'].idxmax(), 'Player'],
                          player_avg_filtered['TO'].max(),
                          "TO")


    functions.awards_tile("Rebound Queen",
                          player_avg_filtered.loc[player_avg_filtered['REB'].idxmax(), 'Player'],
                          player_avg_filtered['REB'].max(),
                          "REB")

    functions.awards_tile("Pick Pocket",
                          player_avg_filtered.loc[player_avg_filtered['STL'].idxmax(), 'Player'],
                          player_avg_filtered['STL'].max(),
                          "STL")

    functions.awards_tile("The Smooth Operator",
                          player_avg_filtered.loc[player_avg_filtered['TS %'].idxmax(), 'Player'],
                          (player_avg_filtered['TS %'].max()*100).round(2),
                          "TS %")

    functions.awards_tile("Three Point Sniper",
                          player_avg_filtered.loc[player_avg_filtered['3PM'].idxmax(), 'Player'],
                          (player_avg_filtered['3PM'].max()),
                          "3PM")

    functions.awards_tile("Best Three Point Shooter",
                          player_avg_filtered.loc[player_avg_filtered['3P %'].idxmax(), 'Player'],
                          (player_avg_filtered['3P %'].max()*100).round(2),
                          "3P %")

    functions.awards_tile("Block Party",
                          player_avg_filtered.loc[player_avg_filtered['BLK'].idxmax(), 'Player'],
                          (player_avg_filtered['BLK'].max()),
                          "BLK")

    functions.awards_tile("Most Winning Player Award",
                          player_avg_filtered.loc[player_avg_filtered['W/L'].idxmax(), 'Player'],
                          (player_avg_filtered['W/L'].max()*100).round(2),
                          "Win %")

    functions.awards_tile("Clutch These 🥜 Award ",
                          player_avg_filtered.loc[player_avg_filtered['GW'].idxmax(), 'Player'],
                          (player_avg_filtered['GW'].max()),
                          "GW")
