import streamlit as st
import plotly.graph_objects as go
import duckdb

def comps():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='../../sat_data.db', read_only=True) 
        print("Working!") 

        # pull total 
        df = con.sql(f"""
            SELECT * FROM total_test_takers;
        """).fetchdf()

        # ******************************
        # streamlit stuff 
        st.title("Comparisons")
        st.markdown("Explore comparisons between states, looking at those whose participation levels either dramatically did or did not reach the same levels as before the COVID-19 pandemic.")

        # arkansas/cali/lousiana/ND/ not really increasing in 2022, 
        st.markdown("Some states, such as Arkansas, Louisiana, and North Dakota, didn't see a return to 'normal levels' of SAT participation in 2022.")

        # use same colors as from Region Trends
        colorss = ['rebeccapurple', 'mediumblue', 'deepskyblue', 'darkturquoise', 'lightseagreen']

        # create dataframe of just the selected state 
        non_inc_states = ['Arkansas', "Louisiana", "North Dakota"]
        dffn = df[(df["State"].isin(non_inc_states))]

        # make line chart
        fig = go.Figure()
        for i, s in enumerate(non_inc_states):
            sdata = dffn[dffn['State'] == s]
            fig.add_trace(go.Scatter(x=sdata["Year"], y=sdata["Total_Test_Takers"], 
                mode='lines', name = s, line = dict(color = colorss[i % len(colorss)])))

        # add titles
        fig.update_layout(
            title = "Certain states do not return to normal levels of SAT participation after the COVID-19 pandemic", 
            xaxis_title = "Year",
            yaxis_title = "Total Number of Test Takers",
            legend_title = "State"
        )

        # add x-axis labels 
        fig.update_xaxes(
            tickvals = [2018, 2019, 2020, 2021, 2022],
            ticktext = ["2018", "2019", "2020", "2021", "2022"],
            range = [2017.9, 2022.2]
        )
        st.plotly_chart(fig, use_container_width=True)


        st.markdown("Some states, such as Colorado, Connecticut, Florida, Georgia, Idaho, Illinois, Iowa, New Mexico, Oklahoma, and Rhode Island, saw a return to 'normal levels' of SAT participation in 2022.")
        st.markdown("Additionally, in some of the states, their levels of participation after the COVID-19 pandemic were higher than before the pandemic.")
        
        # create 2 columns to display plots side by side 
        col1, col2 = st.columns(2)
        
        # create dataframe of just the selected state 
        inc_states = ["Colorado", "Connecticut", "Florida", "Georgia", "Illinois"]
        dffi = df[(df["State"].isin(inc_states))]

        # make line chart
        fig2 = go.Figure()
        for i, s in enumerate(inc_states):
            sdata = dffi[dffi['State'] == s]
            fig2.add_trace(go.Scatter(x=sdata["Year"], y=sdata["Total_Test_Takers"], 
                mode='lines', name = s, line = dict(color = colorss[i % len(colorss)])))

        # add titles
        fig2.update_layout(
            xaxis_title = "Year",
            yaxis_title = "Total Number of Test Takers",
            legend_title = "State"
        )

        # add axes 
        fig2.update_xaxes(
            tickvals = [2018, 2019, 2020, 2021, 2022],
            ticktext = ["2018", "2019", "2020", "2021", "2022"],
            range = [2017.9, 2022.2]
        )
        fig2.update_yaxes(
            tickvals = [25000, 50000, 75000, 100000, 125000, 150000, 175000, 200000],
            ticktext = ['25k', '50k', '75k', '100k', '125k', '150k', '175k', '200k'],
            range = [24000, 201000]
        )
        col1.plotly_chart(fig2, use_container_width=True)

        # second plot 
        inc_states2 = [ "Idaho", "Iowa", "New Mexico", "Oklahoma", "Rhode Island"]
        dffi2 = df[(df["State"].isin(inc_states2))]

        # make line chart
        fig3 = go.Figure()
        for i, s in enumerate(inc_states2):
            sdata = dffi2[dffi2['State'] == s]
            fig3.add_trace(go.Scatter(x=sdata["Year"], y=sdata["Total_Test_Takers"], 
                mode='lines', name = s, line = dict(color = colorss[i % len(colorss)])))

        # add titles
        fig3.update_layout(
            xaxis_title = "Year",
            yaxis_title = "Total Number of Test Takers",
            legend_title = "State"
        )

        # add x-axis labels 
        fig3.update_xaxes(
            tickvals = [2018, 2019, 2020, 2021, 2022],
            ticktext = ["2018", "2019", "2020", "2021", "2022"],
            range = [2017.9, 2022.2]
        )
        fig3.update_yaxes(
            tickvals = [2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000],
            ticktext = ['2.5k', '5k', '7.5k', '10k', '12.5k', '15k', '17.5k', '20k'],
            range = [2400, 22500]
        )
        col2.plotly_chart(fig3, use_container_width=True)

        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    comps()