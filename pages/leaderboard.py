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


functions.load_data()
players = df['Player'].unique().tolist()

player_avg = df.groupby('Player', as_index=False)[df.select_dtypes(include='number').columns].mean()

player_avg = player_avg.sort_values(by="FPS",ascending=False).reset_index(drop=True)
player_avg = player_avg.round(2)



col1, col2 = st.columns(2)

with col1:
    main_container = st.container(border=True)
    main_container.header("👑  Leaderboard")

    for count, row in enumerate(player_avg.itertuples(index=False), start=1):
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
        tile.caption(f'Games Played: **{df[df["Player"] == row.Player].shape[0]}** ')


with col2:
    second_container = st.container(border=True)
    second_container.header("🏆  NBA Awards")

    second_tile = second_container.container(border=True)
    second_tile.subheader('Most Likely to Turn the Ball Over')
    second_tile.write("Xiao")

    third_tile = second_container.container(border=True)
    third_tile.subheader('Most Assist')
    third_tile.write("Sam L.")

    fourth_tile = second_container.container(border=True)
    fourth_tile.subheader('Most Likely to Miss the Shot')
    fourth_tile.write("Wood")

    fifth_tile = second_container.container(border=True)
    fifth_tile.subheader('Most Likely to Chuck a Three')
    fifth_tile.write("Kevin L.")

    sixth_tile = second_container.container(border=True)
    sixth_tile.subheader('Rebound Queen "👩 ')
    sixth_tile.write("Charles")

    seventh_tile = second_container.container(border=True)
    seventh_tile.subheader('Dirty Thief 🥷')
    seventh_tile.write("Lorick")

    # second_tile.functions.awards_tile("🏆", "LeBron James")


st.divider()
st.subheader("Ranked Data")
st.write(player_avg)