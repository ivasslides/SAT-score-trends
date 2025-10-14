import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import duckdb

def states():
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
        st.title("State Trends")
        st.markdown("Explore number of test takers for each state")

        # make dropdown for state options 
        states = df['State'].unique() 
        selected_state = st.selectbox("Select a state:", list(states))

        # create dataframe of just the selected state 
        dff = df[(df["State"] == selected_state)]

        # make line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dff["Year"], y=dff["Total_Test_Takers"], 
        mode='lines', marker_color="blue"))

        # add titles
        fig.update_layout(
            title=f"Total number of SAT test takers in {selected_state}", 
            xaxis_title = "Year",
            yaxis_title="Total Number of Test Takers"
        )

        # add x-axis labels 
        fig.update_xaxes(
            tickvals = [2018, 2019, 2020, 2021, 2022],
            ticktext = ["2018", "2019", "2020", "2021", "2022"],
            range = [2017.9, 2022.2]
        )

        st.plotly_chart(fig, use_container_width=True)

        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    states()