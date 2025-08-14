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
               'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO','GW']

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
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['TS %']:.1%}</td>
                <td>{int(round(row['FGM']))}</td>
                <td>{int(round(row['FGA']))}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['FG %']:.1%}</td>
                <td>{int(round(row['3PM']))}</td>
                <td>{int(round(row['3PA']))}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['3P %']:.1%}</td>
                <td style="background-color: #f2f2f2; font-weight: bold; font-style: italic;">{row['PTS']}</td>
                <td>{int(round(row['REB']))}</td>
                <td>{int(round(row['AST']))}</td>
                <td>{int(round(row['STL']))}</td>
                <td>{int(round(row['BLK']))}</td>
                <td>{int(round(row['TO']))}</td>
                <td>{int(round(row['GW']))}</td>
            </tr>
            </tbody>
        """

    table_html = f"""
            <div style="overflow-x: auto; max-width: 100%;  margin-bottom: 15px;">
                <table style="border-collapse: collapse; table-layout: auto; margin: auto;border: 2px solid #333; ">
                    <thead>
                      <tr>
                        {header_html}
                      </tr>
                    </thead>
                    

                      {row_html}
    """

    return table_html,team_score



def home_button():
    if st.button("Home", use_container_width=True):
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
    if st.button("Career Stats", key='stats-nav', use_container_width=True):
        st.switch_page('pages/career_stats.py')


def leaderboard_button():
    if st.button("Leaderboard", key='leaderboard-nav', use_container_width=True):
        st.switch_page('pages/leaderboard.py')


def awards_tile(award,name,stat_value, stats):
    st.markdown(
        f"""
        <div style="
            display: flex;
            gap: 0.1rem;
            width: 100%;
            max-width: 100%;
            height: auto;
            overflow: visible;
            flex-flow: column;
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(-1px + 1rem);
            font-size: 20px;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        ">
            <div style="font-weight: bold;">{award}</div>
            <div style = "font-size: 20px;" > {name} </div >
            <div style="
                font-family: 'Source Sans', sans-serif;
                font-size: 0.875rem;
                font-weight: 400;
                font-weight: bold;
                line-height: 1.6;
                color: rgba(49, 51, 63, 0.6);
                margin-top: 0px;
                margin-left: 0px;
                margin-right: 0px;
                word-break: break-word;
                text-align: center;
            ">
                {stat_value} {stats}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def career_style():
    return """
    <style>
    /* Table container */
    .vitals-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 2px;
        margin-bottom: 1rem;
        background-color: #fff;
    }

    .vitals-table th, .vitals-table td {
        padding: 4px 10px;
        text-align: left;
        border-width: 1px 0;
        border-style: solid;
        border-color: #f0f0f0;
        background-color: #fff;
    }
    
    .vital-table-th th {
    background-color: #f7f7f7;
    color: #404040;
    font-weight: bold;
    }

    /* Bar chart cells full width */
    td.cell-barchart {
        width: 100%;
        min-width: 150px;
        border: none;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Bar inside cell */
    .barchart-bar {
        height: 0.75rem;             /* small bar height */
        border-radius: 4px;          /* rounded corners */
        background-color: #a3a3a3;   /* default gray background */
        border: 1px solid rgba(0, 0, 0, 0.15); /* subtle border */
        box-sizing: border-box;
    }

    /* Rank colors */
    .barchart-rank-1 { background-color: #2ca02c; } /* green */
    .barchart-rank-2 { background-color: #ff7f0f; } /* orange */
    .barchart-rank-3 { background-color: #1f77b4; } /* blue */

    /* General font styling */
    body, .vitals-table {
        font-family: "Source Sans", sans-serif;
        font-size: 14px;
        line-height: 1.5;
    }
    </style>
    """

def decile_bar(player,max_value):
    pct = player / max_value * 100

    segments_html = ''

    for i in range(10):
        if (i + 1) * 10 <= pct:
            segments_html += f'<div style="width:10%; background-color:#4CAF50; height:16px; border-right:1px solid #fff;"></div>'
        elif i * 10 < pct < (i + 1) * 10:
            segments_html += f'<div style="width:{pct - i * 10}%; background-color:#e0e0e0; height:16px;"></div>'
            segments_html += f'<div style="width:{(i + 1) * 10 - pct}%; background-color:#e0e0e0; height:16px; border-right:1px solid #fff;"></div>'
        else:
            segments_html += f'<div style="width:10%; background-color:#e0e0e0; height:16px; border-right:1px solid #fff;"></div>'

    return f'<div style="display:flex; width:100%;">{segments_html}</div>'