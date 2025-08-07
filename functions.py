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

    columns = ['Player','FPS', 'FGM', 'FGA', 'FG %', '3PM', '3PA', '3P %',
               'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']

    team_score = filtered_df['PTS'].sum()

    header_html = ""
    for i in columns:
        header_html += f'<th> {i} </th>'

    row_html = ""
    for index, row in filtered_df.iterrows():
        row_html += f"""
            <tbody>
            <tr>
                <td>{row['Player']}</td>
                <td>{row['FPS']}</td>
                <td>{row['FGM']}</td>
                <td>{row['FGA']}</td>
                <td>{row['FG%']}</td>
                <td>{row['3PM']}</td>
                <td>{row['3PA']}</td>
                <td>{row['3P %']}</td>
                <td>{row['PTS']}</td>
                <td>{row['REB']}</td>
                <td>{row['AST']}</td>
                <td>{row['STL']}</td>
                <td>{row['BLK']}</td>
                <td>{row['TO']}</td>
            </tr>
            </tbody>
        """



    table_html = f"""
                <div style="overflow-x: auto; width: 100%;">
                  <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                      <tr>
                        {header_html}
                      </tr>
                    </thead>
                    <tbody>
                      {row_html}
    """

    return table_html,team_score