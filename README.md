# SAT-score-trends

- 2017 - 2023 (3 years before pandemic and 3 years after) 
- Total Group & each 50 states
- Total and Section Score -> year, state (or total), combined or section, score interval, number of test takers
- Participation and Score -> year, state (or total), race/ethnicity, number of test takers, percent of total test takers
- Data found at: https://reports.collegeboard.org/sat-suite-program-results/data-archive 


## Process
1. Data sourced from College Board SAT Suite of Assessment Data Archive, for 2018-2022. 
2. PDFs for each state, for each of the 5 years were programatically downloaded locally using Python's requests library. 
3. Using Python's camelot library, the first table on the fifth page of each pdf was parsed and turned into a Pandas dataframe. For each year, all of the states' data were added to a combined dataframe, and then exported as a csv file. 
4. Once each csv file was cleaned and transformed so each had the same column names and such, they were all uploaded into a duckdb database fr easy quering and analytics. 
5. The first analysis done was calculating the total number of test takers in each state, for each year. Additionally, each state's percentage of the total number of test takers in the United States was calculated for each year.  