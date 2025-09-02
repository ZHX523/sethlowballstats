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


def mx_select(selections):
    list_player = pd.Series(True, index=df.index)



    filtered_players = df[list_player]

    subset = df[df["Player"].isin(multiple_select)]
    group_columns = ["Team", "Game", "Date"]
    grouped = subset.groupby(group_columns)

    valid_groups = []

    for name, group in grouped:
        players_in_group = group["Player"].tolist()
        if all(player in players_in_group for player in multiple_select):
            valid_groups.append(name)

    if valid_groups:
        final = subset[group_columns].apply(tuple, axis=1).isin(valid_groups)
        filtered = subset[final]

    return filtered

player_options = df['Player'].unique().tolist()

multiple_select = st.multiselect("Select Multiple Players",
                                 player_options,
                                 max_selections=4)

try:
    filtered_result = mx_select(multiple_select)
    win_rate = (filtered_result['W/L'].sum() / len(multiple_select)) / (
                len(filtered_result['W/L']) / len(multiple_select)) * 100

    st.markdown(f":green-badge[:material/star: Games Won: **{filtered_result['W/L'].sum() / len(multiple_select)}**]"
                f":red-badge[:material/trending_down: Games Lost **{(len(filtered_result['W/L']) / len(multiple_select)) - filtered_result['W/L'].sum() / len(multiple_select)}**]"
                f":violet-badge[:material/sports_basketball: Games Played: **{len(filtered_result['W/L']) / len(multiple_select)}**]"
                f":blue-badge[:material/moving: Win Rate **{win_rate:.2f}%**]")

    columns_to_avg = ["FPS", "TS %", "FGM", "FGA", "FG %", "3PM", "3PA", "3P %",
                      "PTS", "REB", "AST", "STL", "BLK", "TO"]

    for player in multiple_select:
        # Filter stats for this player
        player_df = filtered_result[filtered_result["Player"] == player]

        if not player_df.empty:
            avg_stats = player_df[columns_to_avg].mean().round(2)

            html_stats = (
                '<style>'
                'body {background-color: #f0f4f8;}'
                '.season-stats {display: flex; flex-direction: column; gap: 20px; font-family: Arial, sans-serif;}'
                '.season {background-color: #f0f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;}'
                '.season-year {font-weight: bold; font-size: 18px; margin-bottom: 10px; display: block;}'
                '.stats-row {display: flex; flex-wrap: wrap; gap: 15px;}'
                '.stat {background-color: #f0f4f8; padding: 10px; border-radius: 8px; text-align: center; flex: 1 0 calc(14.28% - 15px);}'
                '.value {font-size: 18px; font-weight: bold; display: block;}'
                '.label abbr {font-size: 12px; color: #555; text-decoration: none;}'
                '</style>'
                f'<div class="season-stats">'
                f'<div class="season"><span class="season-year">{player} Avgs. </span><div class="stats-row">'
            )

            for col in columns_to_avg:
                html_stats += (
                    f'<div class="stat">'
                    f'<span class="value">{avg_stats[col]}</span>'
                    f'<span class="label"><abbr title="{col}">{col}</abbr></span>'
                    f'</div>'
                )

            # Close divs
            html_stats += '</div></div></div>'

            st.markdown(html_stats, unsafe_allow_html=True)


except:
    pass






