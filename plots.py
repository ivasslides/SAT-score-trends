import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st 
import plotly.graph_objects as go
from ipywidgets import interact, widgets
import duckdb 
import logging 

# in terminal: streamlit run plots.py

# logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='plots.log'
)
logger = logging.getLogger(__name__)

def plots():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='sat_data.db', read_only=False) 
        logger.info("Connected to duckdb instance.") 

        # pull total 
        df = con.execute(f"""
            SELECT * FROM total_test_takers;
        """).fetchdf()
        # ******************************
        # streamlit stuff 
        st.title("SAT Participation Dashboard")
        st.markdown("Explore number of test takers by state and year")

        years = [2018, 2019, 2020, 2021, 2022]
        selected_year = st.slider("Select a year, from 2018-2022", min_value=2018, max_value=2022, step=1)

        dff= df[(df['Year'] == selected_year)] 

        fig = go.Figure( 
            data=[go.Bar(
            x=dff["Abbr"], y=dff["Total_Test_Takers"], marker_color="blue")]) 

        fig.update_layout(
            title=f"Total number of SAT test takers for all 50 states in {selected_year}", 
            xaxis_title = "States",
            yaxis_title="Total Number of Test Takers",
            xaxis_tickangle = -45
        )

        st.plotly_chart(fig, use_container_wdith=True)

        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    plots()

