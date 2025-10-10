import requests  
import os
import time 
import logging

# logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='download.log'
)
logger = logging.getLogger(__name__)

# base url for pdfs
early_base = "https://reports.collegeboard.org/media/pdf/{year}-{state}-sat-suite-assessments-annual-report.pdf"

# list of state names 
state_names = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
    "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
    "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey", "new-mexico",
    "new-york", "north-carolina", "north-dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
    "rhode-island", "south-carolina", "south-dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west-virginia", "wisconsin", "wyoming"
]

# make directory for pdfs 
os.makedirs("2018_pdfs", exist_ok=True)
os.makedirs("2019_pdfs", exist_ok=True)
os.makedirs("2020_pdfs", exist_ok=True)
os.makedirs("2021_pdfs", exist_ok=True)
os.makedirs("2022_pdfs", exist_ok=True)

# for 2018-2020 
for y in range(2018, 2021): 
    # for each state, 
    for state in state_names:
        # make url from base url and state name
        url = early_base.format(year=y, state=state)
        # make output path from directory and state name
        out_path = f"{y}_pdfs/{state}.pdf"

        # skip already-downloaded files
        if not os.path.exists(out_path):  
            try:
                # log state name
                logging.info(f"Downloading {y} {state}")
                # get pdf
                r = requests.get(url, timeout=20)
                if r.status_code == 200:
                    with open(out_path, "wb") as f:
                        f.write(r.content)
                # if not work, log error
                else:
                    logging.info(f"Failed to download {y} {state}: {r.status_code}")
            # if error, log error
            except Exception as e:
                logging.info(f"Error with {y} {state}: {e}")
    # pause for 30 seconds and print year
    time.sleep(30)
    print(f"Finished {yr}")

########## different url for 2021 and 2022 reports 
late_base = "https://reports.collegeboard.org/media/pdf/{year}-{state}-sat-suite-of-assessments-annual-report.pdf"
# for 2021-2022 
for y in range(2021, 2023): 
    # for each state, 
    for state in state_names:
        # make url from base url and state name
        url = late_base.format(year=y, state=state)
        # make output path from directory and state name
        out_path = f"{y}_pdfs/{state}.pdf"

        # skip already-downloaded files
        if not os.path.exists(out_path):  
            try:
                # log state name
                logging.info(f"Downloading {y} {state}")
                # get pdf
                r = requests.get(url, timeout=20)
                if r.status_code == 200:
                    with open(out_path, "wb") as f:
                        f.write(r.content)
                # if not work, log error
                else:
                    logging.info(f"Failed to download {y} {state}: {r.status_code}")
            # if error, log error
            except Exception as e:
                logging.info(f"Error with {y} {state}: {e}")
    # pause for 30 seconds and print year 
    time.sleep(30)
    print(f"Finished {yr}")
