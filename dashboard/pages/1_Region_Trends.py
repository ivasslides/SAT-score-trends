import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import duckdb

def regions():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='../sat_data.db', read_only=True) 
        print("Working!") 

        # pull total 
        df = con.execute(f"""
            SELECT * FROM total_test_takers;
        """).fetchdf()

        # *******************************************
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
        dff = df[(df["Year"] == selected_year) & (df["Region"] == selected_region)].copy()

        # color map for states 
        colorss = ['rebeccapurple', 'mediumblue', 'deepskyblue', 'darkturquoise', 'lightseagreen', 'forestgreen', 'springgreen', 'tomato', 'orangered', 'salmon', 'palevioletred', 'orchid', 'hotpink', 'pink']
        
        # make bar chart 
        fig = go.Figure( 
            data=[go.Bar(
            x=dff["Abbr"], y=dff["Total_Test_Takers"], marker_color=colorss)]) 

        # add titles
        fig.update_layout(
            title=f"Total number of SAT test takers for states in the {selected_region} in {selected_year}", 
            xaxis_title = "States",
            yaxis_title="Total Number of Test Takers",
            xaxis_tickangle = -45
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # *******************************************
        # percentages pie charts 
        
        # calculate percentages for each state as part of their region 
        dff["Percentage_of_Region"] = dff["Total_Test_Takers"] / dff["Total_Test_Takers"].sum()
        dff["Percentage_of_Region"] = dff["Percentage_of_Region"].round(2) * 100
        dff["Percentage_of_Region"] = dff["Percentage_of_Region"].astype(int)

        fig = go.Figure(
            data=[go.Pie(
                labels=dff['Abbr'],
                values=dff['Percentage_of_Region'],
                textinfo='label',
                insidetextorientation='radial',
                marker=dict(colors=colorss)
            )]
        ) 
        fig.update_layout(title=f'Percentages of Test Takers by Region in {selected_year}', showlegend=False)

        # creating columns 
        lc, rc = st.columns([2,1])
        # chart on left and text on right 
        with lc:
            st.plotly_chart(fig, use_container_width=True) 
        with rc:
            st.markdown(" ")
            for s in dff['State'].unique():
                pct = dff.loc[dff['State'] == s, 'Percentage_of_Region'].values[0]
                st.markdown(f"{s}: {pct}%")

        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    regions()


