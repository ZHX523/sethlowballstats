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
    if st.button("Home", key='home', use_container_width=True):
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

    td.cell-barchart {
        width: 100%;
        min-width: 150px;
        border: none;
        display: flex;
        align-items: center;
        gap: 4px;
        white-space: nowrap;
        min-width: 0;
    }
    
  
    td.cell-barchart div {
    flex: 1 1 auto;       
    min-width: 20px;
    height: 16px;
    border-radius: 4px;      
    }
    
    td.cell-barchart span {
    white-space: nowrap;  
    font-size: 0.8em;      
    }

    .barchart-bar {
        height: 0.75rem;           
        border-radius: 4px;         
        background-color: #a3a3a3;  
        border: 1px solid rgba(0, 0, 0, 0.15);
        box-sizing: border-box;
    }





    body, .vitals-table {
        font-family: "Source Sans", sans-serif;
        font-size: 16px;
        line-height: 1.5;
    }
    

    @media (max-width: 600px) {
        td.cell-barchart div {
            max-width: 70%;     /* ensure bar doesn't overflow */
        }
        td.cell-barchart span {
            font-size: 0.7em;   /* smaller percentage text */
        }
    }
    
    </style>
    """



    # .barchart-rank-1 { background-color: #2ca02c; } /* green */
    # .barchart-rank-2 { background-color: #ff7f0f; } /* orange */
    # .barchart-rank-3 { background-color: #1f77b4; } /* blue */