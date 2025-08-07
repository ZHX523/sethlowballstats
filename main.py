import streamlit as st
import pandas as pd
import time
import functions


if "data_refreshed" not in st.session_state:
    st.session_state.data_refreshed = False


with st.sidebar:
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.session_state.data_refreshed = True  # flag for success message
        st.rerun()


    df, teams = functions.load_data()

    if st.session_state.data_refreshed:
        st.success("Sucessfully Refreshed")
        time.sleep(2)  # Show message for 2 seconds
        st.session_state.data_refreshed = False
        st.rerun()

    # Sidebar Selectbox 1: Team
    team_options = df['Date'].unique()
    selected_date = st.sidebar.selectbox("Date", team_options)

    # Sidebar Selectbox 2: Player (Filtered by selected team)
    game_options = df[df['Date'] == selected_date]['Game'].unique()
    selected_game = st.sidebar.selectbox("Select a Game", game_options)

    game_id = df[(df['Date'] == selected_date) & (df['Game'] == selected_game)]


row1 = st.columns(1)

for col in row1:
    tile = col.container(border=True)
    tile.header(f'{selected_game} on {selected_date}')
    st.video(game_id.iloc[0]['Video URL'])

st.markdown("""
<style>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
thead {
  background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

for team in teams:
    with st.container(border=True):
        table_html, team_score = functions.build_table_html(df,team,selected_date,selected_game)

        st.subheader(f'Team: {team}', divider=True)
        st.caption(f'Score: **{team_score}** ')
        st.markdown(table_html,unsafe_allow_html=True)



