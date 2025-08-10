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
    functions.refresh_buttion()

    df, teams = functions.load_data()
    st.divider()


st.markdown("""
    <style>
    .sticky-profile {
        position: sticky;
        top: 0;
        padding: 10px 0;
        z-index: 999;

    }
    </style>
""", unsafe_allow_html=True)



player_options = df['Player'].unique().tolist()

selected_player = st.selectbox("***Select a Player***", player_options)

st.divider()

player_df = df[df['Player'] == selected_player]
fps = player_df['FPS'].mean().round(2)

player_profile = st.container()

player_profile.header(f'{selected_player}')
st.markdown(f":green-badge[:material/star: Avg Fantasy Value: **{fps}**]"
            f":violet-badge[:material/sports_basketball: Games Played: **{len(player_df)}**]"
            f":blue-badge[:material/moving: Number of Wins **{player_df['W/L'].sum()}**]"
            f":red-badge[:material/trending_down: Number of Losses **{len(player_df)-player_df['W/L'].sum()}**]")

st.divider()




col1, col2, col3 = st.columns(3)

col_data = [
    (col1, ["PTS", "REB", "AST"]),
    (col2, ["STL", "BLK", "TO"]),
    (col3, ["FG %", "3P %", "TS %"])
]

for col, stats in col_data:
    with col:
        for stat in stats:
            stat_container = st.container(border=True,height=90)

            value = player_df[stat].mean().round(2)

            percent_stats =["FG %", "TS %", "3P %"]

            if stat in percent_stats:
                display_value = f"{value:.1%}"
            else:
                display_value = value

            stat_container.markdown(
                f"""
                <div style="text-align: center; font-weight: bold; font-size: 20px;">
                    {display_value}
                </div>
                """,
                unsafe_allow_html=True
            )

            stat_container.caption(
                f"""
                <p style="text-align: center; font-size: 16px; margin: 0;">
                    {stat}
                </p>
                """,
                unsafe_allow_html=True
            )


