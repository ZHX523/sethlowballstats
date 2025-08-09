import streamlit as st
import pandas as pd
import time





@st.cache_data
def load_data():
    sheet_id = "14KeTtWkhsDyH9D6uq8sB_rpTC_Dt964iqcUy5iC37w4"
    sheet_name = "Sheet1"

    path = csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    df = pd.read_csv(csv_url)
    teams = df['Team'].unique().tolist()
    return df, teams



def build_table_html(df,team,date,game):
    filtered_df = df[
                    (df['Team'] == team) &
                    (df['Date'] == date) &
                    (df['Game'] == game) ]

    columns = ['Player','FPS', 'TS %', 'FGM', 'FGA', 'FG %', '3PM', '3PA', '3P %',
               'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']

    team_score = filtered_df['PTS'].sum()

    header_html = ""
    for i in columns:
        header_html += f'<th style="background-color: #a9a9a9">{i}</th>'

    row_html = ""
    for index, row in filtered_df.iterrows():
        row_html += f"""
            <tbody>
            <tr>
                <td style="width: 150px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" >{row['Player']}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;"> {row['FPS']}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['TS %']}</td>
                <td>{int(round(row['FGM']))}</td>
                <td>{int(round(row['FGA']))}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['FG %']}</td>
                <td>{int(round(row['3PM']))}</td>
                <td>{int(round(row['3PA']))}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['3P %']}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['PTS']}</td>
                <td>{int(round(row['REB']))}</td>
                <td>{int(round(row['AST']))}</td>
                <td>{int(round(row['STL']))}</td>
                <td>{int(round(row['BLK']))}</td>
                <td>{int(round(row['TO']))}</td>
            </tr>
            </tbody>
        """

    table_html = f"""
            <div style="overflow-x: auto; max-width: 100%;">
                <table style="border-collapse: collapse; table-layout: auto; margin: auto;">
                    <thead>
                      <tr>
                        {header_html}
                      </tr>
                    </thead>
                    <tbody>
                      {row_html}
    """

    return table_html,team_score



def home_button():
    if st.button("Home", key='Home-nav', use_container_width=True):
        st.switch_page("main.py")



def refresh_buttion():
    if st.button("Refresh Data",key= 'refresh', use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.session_state.data_refreshed = True
        st.rerun()

    if st.session_state.data_refreshed:
        st.success("Sucessfully Refreshed")
        time.sleep(2)
        st.session_state.data_refreshed = False
        st.rerun()



def career_button():
    if st.button("Career Stats", key='Stats-nav', use_container_width=True):
        st.switch_page('pages/career_stats.py')