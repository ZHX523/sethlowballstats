import streamlit as st
import pandas as pd
import time
import functions
import main
import pages.leaderboard as lb
from functions import decile_bar



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


col1, col2 = st.columns(2)



with col1:
    st.markdown(f"""
    {functions.career_style()}

    <div> 
        <table class="vitals-table" style="border-collapse: collapse; width: 100%;">
            <thead class="vital-table-th">            
                <tr>
                    <th>Stats</th>
                    <th>Avg</th>
                    <th>Avg %</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr> 
            </thead>
            <tbody>
                <tr>
                    <th>PTS</th>
                    <td class="cell-num">{player_df['PTS'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['PTS'].mean(),lb.player_avg['PTS'].max())}</div>
                        <span>{(player_df['PTS'].mean() / lb.player_avg['PTS'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['PTS'].min()}</td>
                    <td class="cell-num">{lb.player_avg['PTS'].max()}</td>
                </tr>
                <tr>
                    <th>REB</th>
                    <td class="cell-num">{player_df['REB'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['REB'].mean(),lb.player_avg['REB'].max())}</div>
                        <span>{(player_df['REB'].mean() / lb.player_avg['REB'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['REB'].min()}</td>
                    <td class="cell-num">{lb.player_avg['REB'].max()}</td>
                </tr>
                <tr>
                    <th>AST</th>
                    <td class="cell-num">{player_df['AST'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['AST'].mean(),lb.player_avg['AST'].max())}</div>
                        <span>{(player_df['AST'].mean() / lb.player_avg['AST'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['AST'].min()}</td>
                    <td class="cell-num">{lb.player_avg['AST'].max()}</td>
                </tr>
                <tr>
                    <th>STL</th>
                    <td class="cell-num">{player_df['STL'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['STL'].mean(),lb.player_avg['STL'].max())}</div>
                        <span>{(player_df['STL'].mean() / lb.player_avg['STL'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['STL'].min()}</td>
                    <td class="cell-num">{lb.player_avg['STL'].max()}</td>
                </tr>
                <tr>
                    <th>BLK</th>
                    <td class="cell-num">{player_df['BLK'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['BLK'].mean(),lb.player_avg['BLK'].max())}</div>
                        <span>{(player_df['BLK'].mean() / lb.player_avg['BLK'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['BLK'].min()}</td>
                    <td class="cell-num">{lb.player_avg['BLK'].max()}</td>
                </tr>
                <tr>
                    <th>TO</th>
                    <td class="cell-num">{player_df['TO'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['TO'].mean(),lb.player_avg['TO'].max())}</div>
                        <span>{(player_df['TO'].mean() / lb.player_avg['TO'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{lb.player_avg['TO'].min()}</td>
                    <td class="cell-num">{lb.player_avg['TO'].max()}</td>
                </tr>
                <tr>
                    <th>FG %</th>
                    <td class="cell-num">{(player_df['FG %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['TO'].mean(),lb.player_avg['TO'].max())}</div>
                        <span>{(player_df['FG %'].mean() / lb.player_avg['FG %'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg['FG %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg['FG %'].max() * 100).round(2)} %</td>
                </tr>
                <tr>
                    <th>3P %</th>
                    <td class="cell-num">{(player_df['3P %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['3P %'].mean(),lb.player_avg['3P %'].max())}</div>
                        <span>{(player_df['3P %'].mean() / lb.player_avg['3P %'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg['3P %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg['3P %'].max() * 100).round(2)} %</td>
                </tr>
                <tr>
                    <th>TS %</th>
                    <td class="cell-num">{(player_df['TS %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['TS %'].mean(),lb.player_avg['TS %'].max())}</div>
                        <span>{(player_df['TS %'].mean() / lb.player_avg['TS %'].max() * 100):.1f}%</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg['TS %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg['TS %'].max() * 100).round(2)} %</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.write('PLACEHOLDER FOR SOMETHING')

# col1, col2, col3 = st.columns(3)
#
# col_data = [
#     (col1, ["PTS", "REB", "AST"]),
#     (col2, ["STL", "BLK", "TO"]),
#     (col3, ["FG %", "3P %", "TS %"])
# ]
#
# for col, stats in col_data:
#     with col:
#         for stat in stats:
#             stat_container = st.container(border=True,height=90)
#
#             value = player_df[stat].mean().round(2)
#
#             percent_stats =["FG %", "TS %", "3P %"]
#
#             if stat in percent_stats:
#                 display_value = f"{value:.1%}"
#             else:
#                 display_value = value
#
#             stat_container.markdown(
#                 f"""
#                 <div style="text-align: center; font-weight: bold; font-size: 20px;">
#                     {display_value}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#
#             stat_container.caption(
#                 f"""
#                 <p style="text-align: center; font-size: 16px; margin: 0;">
#                     {stat}
#                 </p>
#                 """,
#                 unsafe_allow_html=True
#             )
#




