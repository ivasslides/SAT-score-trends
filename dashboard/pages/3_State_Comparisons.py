import streamlit as st
import plotly.graph_objects as go
import duckdb
import os 

def comps():
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
        st.title("Comparisons")
        st.markdown("Explore comparisons between states, looking at those whose participation levels either dramatically did or did not reach the same levels as before the COVID-19 pandemic.")

        # arkansas/cali/lousiana/ND/ not really increasing in 2022, 
        st.markdown("Some states, such as Arkansas, Louisiana, and North Dakota, didn't see a return to 'normal levels' of SAT participation in 2022.")

        # use same colors as from Region Trends
        colorss = ['rebeccapurple', 'mediumblue', 'deepskyblue', 'darkturquoise', 'lightseagreen']

        # create dataframe of just the selected state 
        non_inc_states = ['Arkansas', "Louisiana", "North Dakota"]
        dffn = df[(df["State"].isin(non_inc_states))]
        
        # create 3 columns, with second one biggets to display graph centered 
        col11, col21, col31 = st.columns([1,3,1])

        # make line chart
        fig = go.Figure()
        for i, s in enumerate(non_inc_states):
            sdata = dffn[dffn['State'] == s]
            fig.add_trace(go.Scatter(x=sdata["Year"], y=sdata["Total_Test_Takers"], 
                mode='lines', name = s, line = dict(color = colorss[i % len(colorss)])))

        # adding vertical line at Year 2020 to signal start of pandemic, and emphasizing the drop
        fig.add_vline(
            x=2020, 
            line_width=2, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Start of pandemic",
            annotation_position="top right",
            annotation_font_color="red")
        
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
        col21.plotly_chart(fig, width='stretch')

        st.divider() 
        st.write("\n ")


        # ********************************
        st.markdown("Some states, such as Colorado, Connecticut, Florida, Georgia, Idaho, Illinois, Iowa, New Mexico, Oklahoma, and Rhode Island, saw a return to 'normal levels' of SAT participation in 2022. Additionally, in some of the states, their levels of participation after the COVID-19 pandemic were higher than before the pandemic.")
        
        # making graph title from regular text 
        st.markdown("**States with higher-than-normal levels of SAT participation after the COVID-19 pandemic.**")

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

        # adding vertical line at Year 2020 to signal start of pandemic, and emphasizing the drop
        fig2.add_vline(
            x=2020, 
            line_width=2, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Start of pandemic",
            annotation_position="top right",
            annotation_font_color="red")
        
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
        col1.plotly_chart(fig2, width='stretch')

        # second plot 
        inc_states2 = [ "Idaho", "Iowa", "New Mexico", "Oklahoma", "Rhode Island"]
        dffi2 = df[(df["State"].isin(inc_states2))]

        # make line chart
        fig3 = go.Figure()
        for i, s in enumerate(inc_states2):
            sdata = dffi2[dffi2['State'] == s]
            fig3.add_trace(go.Scatter(x=sdata["Year"], y=sdata["Total_Test_Takers"], 
                mode='lines', name = s, line = dict(color = colorss[i % len(colorss)])))

        # adding vertical line at Year 2020 to signal start of pandemic, and emphasizing the drop
        fig3.add_vline(
            x=2020, 
            line_width=2, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Start of pandemic",
            annotation_position="top right",
            annotation_font_color="red")
        
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
        col2.plotly_chart(fig3, width='content')

        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    comps()