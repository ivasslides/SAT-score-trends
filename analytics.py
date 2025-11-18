import duckdb 
import logging

# logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='analytics.log'
)
logger = logging.getLogger(__name__)

def analytics():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='sat_data.db', read_only=False) 
        logger.info("Connected to duckdb instance.") 

        # calculate total number of test takers for each state, for each year, as new table 
        con.execute(f"""
            DROP TABLE IF EXISTS total_test_takers;
            CREATE TABLE total_test_takers(
                State TEXT, Year INTEGER, Total_Test_Takers INTEGER);
        """)
        logging.info("Empty table created.")

        # insert state, year, and total test taker values into table
        con.execute(f"""
        INSERT INTO total_test_takers (State, Year, Total_Test_Takers)
        SELECT State, Year, SUM(Total)
                FROM (
                    SELECT * FROM averages_2018 
                    UNION ALL
                    SELECT * FROM averages_2019 
                    UNION ALL
                    SELECT * FROM averages_2020 
                    UNION ALL
                    SELECT * FROM averages_2021 
                    UNION ALL 
                    SELECT * FROM averages_2022 
                ) AS Total_Test_Takers
            GROUP BY State, Year
            ORDER BY Year, State; 
        """)
        logging.info("Totals added.")

        # calculate each state's percentage of the total total number, rounded to 2 decimal places
        con.execute(f"""
            ALTER TABLE total_test_takers
            ADD COLUMN Percentage_of_Total FLOAT;

            UPDATE total_test_takers
            SET Percentage_of_Total = ROUND(
                (Total_Test_Takers * 100.0) / 
                (SELECT SUM(t2.Total_Test_Takers)
                    FROM total_test_takers AS t2 
                    WHERE t2.Year = total_test_takers.Year)
                , 2
            );
        """)
        logging.info("Percentages added.")

        # making new table w state abbreviations and regions and add to exisitng table
        con.execute(f"""
            DROP TABLE IF EXISTS state_info; 

            CREATE TABLE state_info (
                Name VARCHAR, Abbr CHAR(2), Region VARCHAR);

                INSERT INTO state_info VALUES 
                ('Alabama', 'AL', 'South'), ('Alaska', 'AK', 'West'), ('Arizona', 'AZ', 'West'), ('Arkansas', 'AR', 'South'), ('California', 'CA', 'West'), ('Colorado', 'CO', 'West'), ('Connecticut', 'CT', 'Northeast'), 
                ('Delaware', 'DE', 'Northeast'), ('Florida', 'FL', 'South'), ('Georgia', 'GA', 'South'), ('Hawaii', 'HI', 'West'), ('Idaho', 'ID', 'West'), ('Illinois', 'IL', 'Midwest'), ('Indiana', 'IN', 'Midwest'),  
                ('Iowa', 'IA', 'Midwest'), ('Kansas', 'KS', 'Midwest'), ('Kentucky', 'KY', 'South'), ('Louisiana', 'LA', 'South'), ('Maine', 'ME', 'Northeast'), ('Maryland', 'MD', 'Northeast'), ('Massachusetts', 'MA', 'Northeast'),
                ('Michigan', 'MI', 'Midwest'), ('Minnesota', 'MN', 'Midwest'), ('Mississippi', 'MS', 'South'), ('Missouri', 'MO', 'Midwest'), ('Montana', 'MT', 'West'), ('Nebraska', 'NE', 'Midwest'), ('Nevada', 'NV', 'West'), 
                ('New Hampshire', 'NH', 'Northeast'), ('New Jersey', 'NJ', 'Northeast'), ('New Mexico', 'NM', 'West'), ('New York', 'NY', 'Northeast'), ('North Carolina', 'NC', 'South'), ('North Dakota', 'ND', 'Midwest'), 
                ('Ohio', 'OH', 'Midwest'), ('Oklahoma', 'OK', 'South'), ('Oregon', 'OR', 'West'), ('Pennsylvania', 'PA', 'Northeast'), ('Rhode Island', 'RI', 'Northeast'), ('South Carolina', 'SC', 'South'), ('South Dakota', 'SD', 'Midwest'),
                ('Tennessee', 'TN', 'South'), ('Texas', 'TX', 'South'), ('Utah', 'UT', 'West'), ('Vermont', 'VT', 'Northeast'), ('Virginia', 'VA', 'South'), ('Washington', 'WA', 'West'), ('West Virginia', 'WV', 'South'), 
                ('Wisconsin', 'WI', 'Midwest'), ('Wyoming', 'WY', 'West'); 

                ALTER TABLE total_test_takers ADD COLUMN Abbr CHAR(2);
                ALTER TABLE total_test_takers ADD COLUMN Region VARCHAR;

                UPDATE total_test_takers
                SET Abbr = s.Abbr, 
                    Region = s.Region
                FROM state_info s 
                    WHERE total_test_takers.State = s.Name; 
        """)
        logging.info("State abbrs and regions added.")

        con.close()
        


    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    analytics()