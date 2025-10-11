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
                ('alabama', 'AL', 'South'), ('alaska', 'AK', 'West'), ('arizona', 'AZ', 'West'), ('arkansas', 'AR', 'South'), ('california', 'CA', 'West'), ('colorado', 'CO', 'West'), ('connecticut', 'CT', 'Northeast'), 
                ('delaware', 'DE', 'Northeast'), ('florida', 'FL', 'South'), ('georgia', 'GA', 'South'), ('hawaii', 'HI', 'West'), ('idaho', 'ID', 'West'), ('illinois', 'IL', 'Midwest'), ('indiana', 'IN', 'Midwest'),  
                ('iowa', 'IA', 'Midwest'), ('kansas', 'KS', 'Midwest'), ('kentucky', 'KY', 'South'), ('louisiana', 'LA', 'South'), ('maine', 'ME', 'Northeast'), ('maryland', 'MD', 'Northeast'), ('massachusetts', 'MA', 'Northeast'),
                ('michigan', 'MI', 'Midwest'), ('minnesota', 'MN', 'Midwest'), ('mississippi', 'MS', 'South'), ('missouri', 'MO', 'Midwest'), ('montana', 'MT', 'West'), ('nebraska', 'NE', 'Midwest'), ('nevada', 'NV', 'West'), 
                ('new-hampshire', 'NH', 'Northeast'), ('new-jersey', 'NJ', 'Northeast'), ('new-mexico', 'NM', 'West'), ('new-york', 'NY', 'Northeast'), ('north-carolina', 'NC', 'South'), ('north-dakota', 'ND', 'Midwest'), 
                ('ohio', 'OH', 'Midwest'), ('oklahoma', 'OK', 'South'), ('oregon', 'OR', 'West'), ('pennsylvania', 'PA', 'Northeast'), ('rhode-island', 'RI', 'Northeast'), ('south-carolina', 'SC', 'South'), ('south-dakota', 'SD', 'Midwest'),
                ('tennessee', 'TN', 'South'), ('texas', 'TX', 'South'), ('utah', 'UT', 'West'), ('vermont', 'VT', 'Northeast'), ('virginia', 'VA', 'South'), ('washington', 'WA', 'West'), ('west-virginia', 'WV', 'South'), 
                ('wisconsin', 'WI', 'Midwest'), ('wyoming', 'WY', 'West'); 

                ALTER TABLE total_test_takers ADD COLUMN Abbr CHAR(2);
                ALTER TABLE total_test_takers ADD COLUMN Region VARCHAR;

                UPDATE total_test_takers
                SET Abbr = s.Abbr, 
                    Region = s.Region
                FROM state_info s 
                    WHERE total_test_takers.State = s.Name; 
        """)
        logging.info("State abbrs and regions added.")


    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    analytics()