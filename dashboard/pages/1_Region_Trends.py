import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import duckdb

def regions():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='/home/ivasslides/SAT-score-trends/sat_data.db', read_only=True) 
        print("Working!") 

        # pull total 
        df = con.execute(f"""
            SELECT * FROM total_test_takers;
        """).fetchdf()

        # ******************************
        # streamlit stuff 
        st.title("Region Trends")
        st.markdown("Explore number of test takers by region and year")

        # make slider to select a year
        years = [2018, 2019, 2020, 2021, 2022]
        selected_year = st.slider("Select a year:", min_value=2018, max_value=2022, step=1)
        
        # make dropdown to select a region 
        regions = df['Region'].unique() 
        selected_region = st.selectbox("Select a region:", list(regions))

        # make dataframe with just selected year and region 
        dff = df[(df["Year"] == selected_year) & (df["Region"] == selected_region)]

        # make bar chart 
        fig = go.Figure( 
            data=[go.Bar(
            x=dff["Abbr"], y=dff["Total_Test_Takers"], marker_color="blue")]) 

        # add titles
        fig.update_layout(
            title=f"Total number of SAT test takers for states in the {selected_region} in {selected_year}", 
            xaxis_title = "States",
            yaxis_title="Total Number of Test Takers",
            xaxis_tickangle = -45
        )

        st.plotly_chart(fig, use_container_width=True)

        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    regions()


