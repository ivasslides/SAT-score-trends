import streamlit as st
import plotly.graph_objects as go
import duckdb
import os 

def states():
    con = None

    # make path to db based on current file path 
    DB_PATH = os.path.join(os.path.dirname(__file__), '../..', 'sat_data.db')

    try:
        con = duckdb.connect(database=DB_PATH, read_only=True)
        # st.success(f"Connection SUCCESS! Path checked: {DB_PATH}")
        print("Working!") 

        # pull total 
        df = con.sql(f"""
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

        # create 3 columns, with second one biggets to display graph centered 
        col1, col2, col3 = st.columns([1,3,1])

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

        col2.plotly_chart(fig, width='stretch')

        # ******************************

        # pull average table for each year  
        df18 = con.execute(f"""
            SELECT * FROM averages_2018;
        """).fetchdf()
        df19 = con.execute(f"""
            SELECT * FROM averages_2019;
        """).fetchdf()
        df20 = con.execute(f"""
            SELECT * FROM averages_2020;
        """).fetchdf()
        df21 = con.execute(f"""
            SELECT * FROM averages_2021;
        """).fetchdf()
        df22 = con.execute(f"""
            SELECT * FROM averages_2022;
        """).fetchdf()

        # display number of test takers for each interval 
        st.divider() 

        st.subheader("Distribution of Test Takers Across Different Score Intervals")
        st.markdown("The charts below show the distribution across the total score intervals for each of the five years. The highest possible score is 1600 (on the right) and the lowest possible score is 400 (on the left).")
        st.markdown("Even though the number of test takers who fall into each score interval vary across the years, the distribution is similar for every year. It is reasonable to expect that the median score range is the same, or very close to the same, for each year. This shows that although the number of test takers decline after the pandemic, the skill level of the test takers remain mostly stable.")

        # show bar chart for each year 
        df18_s = df18[(df18["State"] == selected_state)]
        df19_s = df19[(df19["State"] == selected_state)]
        df20_s = df20[(df20["State"] == selected_state)]
        df21_s = df21[(df21["State"] == selected_state)]
        df22_s = df22[(df22["State"] == selected_state)]

        # array with intervals in ascending order 
        interval_order = ['400-590', '600-790', '800-990', '1000-1190', '1200-1390', '1400-1600']

        lc, rc = st.columns(2)
        with lc:
            # 2018 
            fig = go.Figure( 
                data=[go.Bar(
                    x=df18_s["Total Score Interval"], y=df18_s["Total"], marker_color='lightblue')]) 
            fig.update_xaxes(categoryorder='array', categoryarray=interval_order)
            fig.update_layout(title=f'Total Score Intervals for {selected_state} in 2018')
            st.plotly_chart(fig, width='content')

            # 2020 
            fig = go.Figure( 
                data=[go.Bar(
                    x=df20_s["Total Score Interval"], y=df20_s["Total"], marker_color='lightgreen')]) 
            fig.update_xaxes(categoryorder='array', categoryarray=interval_order)
            fig.update_layout(title=f'Total Score Intervals for {selected_state} in 2020')
            st.plotly_chart(fig, width='content')

            # 2022
            fig = go.Figure( 
                data=[go.Bar(
                    x=df22_s["Total Score Interval"], y=df22_s["Total"], marker_color='orchid')]) 
            fig.update_xaxes(categoryorder='array', categoryarray=interval_order)
            fig.update_layout(title=f'Total Score Intervals for {selected_state} in 2022')
            st.plotly_chart(fig, width='content')

        with rc:
            # 2019 
            fig = go.Figure( 
                data=[go.Bar(
                    x=df19_s["Total Score Interval"], y=df19_s["Total"], marker_color='lightpink')]) 
            fig.update_xaxes(categoryorder='array', categoryarray=interval_order)
            fig.update_layout(title=f'Total Score Intervals for {selected_state} in 2019')
            st.plotly_chart(fig, width='content')

            # 2021 
            fig = go.Figure( 
                data=[go.Bar(
                    x=df21_s["Total Score Interval"], y=df21_s["Total"], marker_color='yellow')]) 
            fig.update_xaxes(categoryorder='array', categoryarray=interval_order)
            fig.update_layout(title=f'Total Score Intervals for {selected_state} in 2021')
            st.plotly_chart(fig, width='content')
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    states()