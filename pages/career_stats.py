import streamlit as st
import pandas as pd
import time
import functions
import main
import math
import pages.leaderboard as lb
from functions import decile_bar
import plotly.graph_objects as go


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
st.caption("***15 Game Min.***")



functions.load_data()
players = df['Player'].unique().tolist()

player_avg = df.groupby('Player', as_index=False)[df.select_dtypes(include='number').columns].mean()

player_avg = player_avg.sort_values(by="FPS",ascending=False).reset_index(drop=True)
player_avg = player_avg.round(2)

games_per_player = df.groupby("Player").size()
valid_players = games_per_player[games_per_player >= 15].index
player_avg_filtered = player_avg[player_avg['Player'].isin(valid_players)]



player_df = df[df['Player'] == selected_player]
fps = player_df['FPS'].mean().round(2)


col1, col2 = st.columns(2)

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"



with col1:
    player_profile = st.container()

    player_profile.header(f'{selected_player}')
    st.markdown(f":green-badge[:material/star: Avg Fantasy Value: **{fps}**]"
                f":violet-badge[:material/sports_basketball: Games Played: **{len(player_df)}**]"
                f":blue-badge[:material/moving: Number of Wins **{player_df['W/L'].sum()}**]"
                f":red-badge[:material/trending_down: Number of Losses **{len(player_df) - player_df['W/L'].sum()}**]")

    st.markdown(f"""
    {functions.career_style()}

    <div> 
        <table class="vitals-table" style="border-collapse: collapse; width: 100%;">
            <thead class="vital-table-th">            
                <tr>
                    <th>Stats</th>
                    <th>Avg</th>
                    <th>Percentile</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr> 
            </thead>
            <tbody>
                <tr>
                    <th>PTS</th>
                    <td class="cell-num">{player_df['PTS'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['PTS'].mean(),lb.player_avg_filtered['PTS'].max())}</div>
                        <span>{ordinal(math.floor((player_df['PTS'].mean() / lb.player_avg_filtered['PTS'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['PTS'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['PTS'].max()}</td>
                </tr>
                <tr>
                    <th>REB</th>
                    <td class="cell-num">{player_df['REB'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['REB'].mean(),lb.player_avg_filtered['REB'].max())}</div>
                        <span>{ordinal(math.floor((player_df['REB'].mean() / lb.player_avg_filtered['REB'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['REB'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['REB'].max()}</td>
                </tr>
                <tr>
                    <th>AST</th>
                    <td class="cell-num">{player_df['AST'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['AST'].mean(),lb.player_avg_filtered['AST'].max())}</div>
                        <span>{ordinal(math.floor((player_df['AST'].mean() / lb.player_avg_filtered['AST'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['AST'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['AST'].max()}</td>
                </tr>
                <tr>
                    <th>STL</th>
                    <td class="cell-num">{player_df['STL'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['STL'].mean(),lb.player_avg_filtered['STL'].max())}</div>
                        <span>{ordinal(math.floor((player_df['STL'].mean() / lb.player_avg_filtered['STL'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['STL'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['STL'].max()}</td>
                </tr>
                <tr>
                    <th>BLK</th>
                    <td class="cell-num">{player_df['BLK'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['BLK'].mean(),lb.player_avg_filtered['BLK'].max())}</div>
                        <span>{ordinal(math.floor((player_df['BLK'].mean() / lb.player_avg_filtered['BLK'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['BLK'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['BLK'].max()}</td>
                </tr>
                <tr>
                    <th>TO</th>
                    <td class="cell-num">{player_df['TO'].mean().round(2)}</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['TO'].mean(),lb.player_avg_filtered['TO'].max())}</div>
                        <span>{ordinal(math.floor((player_df['TO'].mean() / lb.player_avg_filtered['TO'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{lb.player_avg_filtered['TO'].min()}</td>
                    <td class="cell-num">{lb.player_avg_filtered['TO'].max()}</td>
                </tr>
                <tr>
                    <th>FG %</th>
                    <td class="cell-num">{(player_df['FG %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['FG %'].mean(),lb.player_avg_filtered['FG %'].max())}</div>
                        <span>{ordinal(math.floor((player_df['FG %'].mean() / lb.player_avg_filtered['FG %'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg_filtered['FG %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg_filtered['FG %'].max() * 100).round(2)} %</td>
                </tr>
                <tr>
                    <th>3P %</th>
                    <td class="cell-num">{(player_df['3P %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['3P %'].mean(),lb.player_avg_filtered['3P %'].max())}</div>
                        <span>{ordinal(math.floor((player_df['3P %'].mean() / lb.player_avg_filtered['3P %'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg_filtered['3P %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg_filtered['3P %'].max() * 100).round(2)} %</td>
                </tr>
                <tr>
                    <th>TS %</th>
                    <td class="cell-num">{(player_df['TS %'].mean() * 100).round(1)} %</td>
                    <td class="cell-barchart" style="display: flex; align-items: center; gap: 4px;">
                        <div style="display:flex; width:100%;">{functions.decile_bar(player_df['TS %'].mean(),lb.player_avg_filtered['TS %'].max())}</div>
                        <span>{ordinal(math.floor((player_df['TS %'].mean() / lb.player_avg_filtered['TS %'].max()) * 10))}</span>
                    </td>
                    <td class="cell-num">{(lb.player_avg_filtered['TS %'].min() * 100).round(2)} %</td>
                    <td class="cell-num">{(lb.player_avg_filtered['TS %'].max() * 100).round(2)} %</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col2:
    stat_profile = st.container()

    stat_profile.header(f'{selected_player} Profile')

    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
    values = [math.floor((player_df['PTS'].mean() / lb.player_avg_filtered['PTS'].max()) * 10),
              math.floor((player_df['REB'].mean() / lb.player_avg_filtered['REB'].max()) * 10),
              math.floor((player_df['AST'].mean() / lb.player_avg_filtered['AST'].max()) * 10),
              math.floor((player_df['STL'].mean() / lb.player_avg_filtered['STL'].max()) * 10),
              math.floor((player_df['BLK'].mean() / lb.player_avg_filtered['BLK'].max()) * 10),
              math.floor((player_df['TO'].mean() / lb.player_avg_filtered['TO'].max()) * 10)]

    values += values[:1]
    categories += categories[:1]

    # Create radar chart
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                fillcolor='rgba(144, 238, 144, 0.4)',
                line=dict(color='rgba(60, 179, 113, 1)', width=2)
            )
        ]
    )

    # Update layout
    fig.update_layout(
        polar=dict(
            bgcolor='#ebebeb',
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            ),
            angularaxis=dict(
                visible=True
            ),
            gridshape='linear'
        ),
        height=340,
        margin=dict(t=20, b=0, l=5, r=5),
        paper_bgcolor='white'
    )

    st.plotly_chart(fig,use_container_width=True,config={'staticPlot': True})





st.divider()
st.subheader("Ranked Data - Averages")
st.write(player_avg)


