import pandas as pd 
import camelot 
import glob 
import os 
import numpy as np 
import logging
import duckdb 

# logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)

# function to shift all rows to left-most column 
def shift_row_left(row):
    # convert all cells to string
    row_str = row.astype(str)
    # find non-empty cells 
    non_empty = row_str[row_str.str.strip() != ""]
    # fill row with non-empty values 
    new_row = pd.Series(list(non_empty) + [np.nan]*(len(row) - len(non_empty)))
    return new_row

# ********************************************
# ********************************************

# function to pull tables from pdfs and convert to csv files 
def convert_to_csv():
    # pull all pdf files 
    files_2018 = glob.glob("2018_pdfs/*.pdf")
    files_2019 = glob.glob("2019_pdfs/*.pdf")
    files_2020 = glob.glob("2020_pdfs/*.pdf")
    files_2021 = glob.glob("2021_pdfs/*.pdf")
    files_2022 = glob.glob("2022_pdfs/*.pdf")

    # list of files and years 
    files = [files_2018, files_2019, files_2020, files_2021, files_2022]
    years = [2018, 2019, 2020, 2021, 2022]

    print("starting up...")
    # for all years and files, 
    for yr, y_files in zip(years, files):
        # create empty df
        all_tables = []

        # for each file in files 
        for f in y_files: 
            # pull state name 
            state = os.path.basename(f).replace(".pdf", "")
            try: 
                # pull tables from pdf, 2022 gets page 7 
                if yr == 2022: 
                    t = camelot.read_pdf(f, pages='7', flavor="stream")
                else: 
                    t = camelot.read_pdf(f, pages='5', flavor="stream")
                logging.info(f"{state} {yr} table: {len(t)}")
                # keep only first table in df
                df = t[0].df

                # drop columns w percentages
                col_w_p = [
                    col for col in df.columns
                    if df[col].astype(str).str.contains('%').any()
                ]
                df = df.drop(columns=col_w_p)
                # rename colummns
                df.columns = range(df.shape[1])

                # drop rows that have unwanted string values 
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Mean', case=False, na=False).any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('SD', case=False, na=False).any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('_________________________________________________________', 
                        case=False, na=False).any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Total and Section Scores', case=False, na=False).any(), axis=1)]
                # esp for 2018 
                df = df[~df.apply(lambda row: row.astype(str).str.contains('is summarized', case=False, na=False).any(), axis=1)]
                # esp for 2019
                df = df[~df.apply(lambda row: row.astype(str).str.contains('issummarized', case=False, na=False).any(), axis=1)]
                # esp for 2020
                df = df[~df.apply(lambda row: row.astype(str).str.contains('is	summarized.', case=False, na=False).any(), axis=1)]            
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Total', case=False, na=False).any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('EWR', case=False, na=False).any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Math', case=False, na=False).any(), axis=1)]

                # shift rows that have whitespace in first column
                df = df.apply(lambda row: shift_row_left(row) if str(row.iloc[0]).strip() == "" or str(row.iloc[0]).lower() == "nan" else row, axis=1)
                # drop fully empty columns after shifting
                df = df.dropna(axis=1, how='all')
                # reset index
                df = df.reset_index(drop=True)

                # add column names
                df.columns = ["Total Score Interval", "Total", "Score Interval", "EWR",
                            "Math"]

                # fix score interval values 
                df['Total Score Interval'] = df['Total Score Interval'].replace({'â€“': '-', '–': '-', '—': '-'}, regex=True)
                df['Score Interval'] = df['Score Interval'].replace({'â€“': '-', '–': '-', '—': '-'}, regex=True)
                
                # clean number of test taker columns, and change to ints 
                # if is null or empty string, make 0 
                for i in range(df.shape[1]):
                    if pd.isna(df.loc[i, 'Total']) or df.loc[i, 'Total'] == '':
                        df.loc[i, 'Total'] = 0
                    if pd.isna(df.loc[i, 'EWR']) or df.loc[i, 'EWR'] == '':
                        df.loc[i, 'EWR'] = 0
                    if pd.isna(df.loc[i, 'Math']) or df.loc[i, 'Math'] == '':
                        df.loc[i, 'Math'] = 0

                # remove commas, spaces, empties, and change to ints 
                df['Total'] = df['Total'].astype(str).str.replace(',', '', regex=False).str.replace(r'(?<=\d)\s+(?=\d)', '', regex=True).replace('', 0).replace(' ', 0).astype(float).astype('Int64')
                df['EWR'] = df['EWR'].astype(str).str.replace(',', '', regex=False).str.replace(r'(?<=\d)\s+(?=\d)', '', regex=True).replace('', 0).replace(' ', 0).astype(float).astype('Int64')
                df['Math'] = df['Math'].astype(str).str.replace(',', '', regex=False).str.replace(r'(?<=\d)\s+(?=\d)', '', regex=True).replace('', 0).replace(' ', 0).astype(float).astype('Int64')

                # add state and year columns to df
                df['State'] = state
                df['Year'] = yr

                # append to giant table
                all_tables.append(df) 
                
            # if error, print error and continue
            except Exception as e:
                logging.info(f"error with {state}: {e}")
                print(f"error with {state}: {e}")
                continue

        # combine into big df 
        final_df = pd.concat(all_tables, ignore_index=True)
        # export to csv 
        final_df.to_csv(f"{yr}_averages.csv", index=False)
        print(f"Finished {yr}")

# ********************************************
# ********************************************

# function to upload all csvs to duckdb -> sat_data.db 
def upload():
    con = None

    try: 
        # create and verify connection 
        con = duckdb.connect(database='sat_data.db', read_only=False) 
        logger.info("Connected to duckdb instance") 
        print("Connected to duckdb instance")

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
    convert_to_csv() 
    upload()
