import streamlit as st 
import duckdb
import pandas as pd

# in terminal, in dashboard dir : streamlit run Home.py


# table showing total number of test takers for each region, per year 
def homes():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='/home/ivasslides/SAT-score-trends/sat_data.db', read_only=True) 

        # making title
        st.title("SAT Trends in the US")

        # add text
        st.write("""
            Welcome to the SAT Trends Dashboard!
            \n Use the sidebar to navigate beween: 
            \n - **Region Trends**: examine SAT participation in each state, grouped by region and year
            \n - **State Trends**: explore trends in the total number of SAT test takers and in score performance for each state
            \n - **State Comparisons**: compare the total number of SAT test takers across states after the COVID-19 pandemic
        """)

        st.divider()
        # *************************************
        # display some quick highlights/summary 
        st.markdown("To gain a quick overview of SAT participation and score trends in the US, below is a table summarizing the total number of test takers for each region over time.")
        
        # aggregate by region and year to create dataframe  
        df = con.execute(f"""
            SELECT Year, Region, SUM("Total_Test_Takers") AS Totals
            FROM total_test_takers
            GROUP BY Year, Region
            ORDER BY Year, Region;
        """).fetchdf()

        # turn pivot dataframe to have index and columns for streamlit table 
        df_pivot = df.pivot(index = 'Region', columns = 'Year', values = 'Totals') 
        # remove decimal places, and ensure thousands comma is there 
        df_pivot = df_pivot.map(lambda x: f"{int(x):,}")

        # list of colors 
        colors = ['lightblue', 'lightgreen', 'orchid', 'lightpink', 'lightgray']
        # using lambda function to apply different color to each column, aka each year 
        styled_df = df_pivot.style.apply(
            lambda col: ['background-color: {}'.format(colors[i % len(colors)]) for i in range(len(col))],
             axis = 1)

        # create table from dataframe 
        st.table(data=styled_df, border=True)

        # *************************************
        # 

        # display imge 
        st.image('https://inside.nku.edu/content/inside/testing/tests/entrance-exam/SAT/_jcr_content/par/columncontrol/column-2/textimage/image.img.jpg/1763587190.jpg', width = 'stretch')



        print("Working!") 

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    homes()






