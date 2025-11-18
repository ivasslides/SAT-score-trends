import streamlit as st
import plotly.graph_objects as go
import duckdb
import os 

def regions():
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

        st.plotly_chart(fig, width='stretch')

        st.divider()

        # *******************************************
        # percentages pie charts 

        st.subheader("Percentage of the Region")
        st.markdown("The pie chart below displays each state's percentage of the total number of tets takers in the region. The same colors correspond to those in the graph above. Additionally the legend explicitly lists the percentages for each state as well. The largest and most populated state(s) show the highest percentage of the region, regardless of how many states are included in that region.")

        
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
            st.plotly_chart(fig, width='stretch') 
        with rc:
            st.markdown(" ")
            for s in dff['State'].unique():
                pct = dff.loc[dff['State'] == s, 'Percentage_of_Region'].values[0]
                st.markdown(f"{s}: {pct}%")

        
    except Exception as e:
        st.error(f"Error accessing database at: {DB_PATH}. Traceback: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    regions()


