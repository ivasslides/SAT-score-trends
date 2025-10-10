import duckdb
import os
import logging

# logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='upload.log'
)
logger = logging.getLogger(__name__)

# function to upload all csvs to duckdb -> sat_data.db 
def upload():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='sat_data.db', read_only=False) 
        logger.info("Connected to duckdb instance") 

        # loading 2018 into duckdb
        con.execute(f"""
            DROP TABLE IF EXISTS averages_2018;
            CREATE TABLE averages_2018 AS
            SELECT * FROM read_csv("./2018_averages.csv");
        """)
        logging.info("Successfully loaded 2018 averages.")
        
        # loading 2019 into duckdb
        con.execute(f"""
            DROP TABLE IF EXISTS averages_2019;
            CREATE TABLE averages_2019 AS 
            SELECT * from read_csv("./2019_averages.csv");
        """)
        logging.info("Successfully loaded 2019 averages.")

        # loading 2020 into duckdb
        con.execute(f"""
            DROP TABLE IF EXISTS averages_2020;
            CREATE TABLE averages_2020 AS
            SELECT * from read_csv("./2020_averages.csv");
        """)
        logging.info("Successfully loaded 2020 averages.")

        # loading 2021 into duckdb
        con.execute(f"""
            DROP TABLE IF EXISTS averages_2021;
            CREATE TABLE averages_2021 AS
            SELECT * FROM read_csv("./2021_averages.csv");
        """)
        logging.info("Successfully loaded 2021 averages.")

        # loading 2022 into duckdb
        con.execute(f"""
            DROP TABLE IF EXISTS averages_2022;
            CREATE TABLE averages_2022 AS
            SELECT * FROM read_csv("./2022_averages.csv")
        """)
        logging.info("Successfully loaded 2022 averages.")


    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    upload()
