from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# creating a list of teams and years to loop through for scraping data from multiple pages
teams = [
    "ATL", "PHI", "WSN", "MIA", "NYM", "NYY", "TBR", "TOR", "BAL", "BOS",
    "CIN", "PIT", "STL", "MIL", "CHC", "CWS", "CLE", "DET", "KC", "MIN", 
    "ARI", "COL", "LAD", "SDP", "SFG", "OAK", "SEA", "HOU", "LAA", "TEX"
    ]
# creating a list of years to loop through for scraping data from multiple pages
years = range(2020, 2027)

master_list = []
# looping through each team and year to scrape the data and store it in a dataframe, 
# then transfer it to a csv file
for team in teams:
    for year in years:
        print(f"Scraping data for {team} in {year}...")

        # Construct the URL for the team's batting statistics page for the given year
        url = f"https://www.baseball-reference.com/teams/{team}/{year}.shtml"
        
        html_page = requests.get(url)

        # Adding a delay between requests to avoid overwhelming the server
        time.sleep(3)
        
        # Check if the request was successful
        if html_page.status_code != 200:
            print(f"Failed to retrieve data for {team} in {year}. Status code: {html_page.status_code}")
            continue

        html_page.encoding = "utf-8" # <-- this accounts for the special char in names
        team_html = BeautifulSoup(html_page.text, "html.parser")

        team_tables = team_html.find('table', id='players_standard_batting')

        # If the table is not found, skip to the next iteration
        if team_tables is None:
            print(f"No batting data found for {team} in {year}. Skipping...")
            continue

        table_titles = team_tables.find('thead').find_all('th')

        categories = [title.text.strip() for title in table_titles]
        # removes the duplicate 'POS' column that appears in the table
        categories.pop(-2)

        team_dataframe = pd.DataFrame(columns = categories)

        # Getting all the table data
        all_data = team_tables.find_all('tr')

        # Cleaning the data
        for each_row in all_data:
            row_header = each_row.find('th')

            if row_header is None:
                continue

            row_data = each_row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]

            # Skip empty rows
            if len(individual_row_data) == 0:
                continue
            
            rank = row_header.text.strip()

            # Skip repeated header rows
            if rank == 'Rk':
                continue

            individual_row_data.insert(0, rank)
            # removes the values in the duplicate 'POS' column that appears in the table
            individual_row_data.pop(-2)

            # To remove pitcher names from coming up in the batting data, we can skip
            # over any rows that include "P" in the position column (Pos)
            # Find the position column
            pos_index = categories.index('Pos')

            # Skip pitchers
            if individual_row_data[pos_index] == 'P':
                continue

            # Clean player names
            player_name = individual_row_data[1]

            player_name = player_name.replace("*", "")
            player_name = player_name.replace("#", "")

            # Remove anything inside parentheses
            player_name = player_name.split("(")[0].strip()

            individual_row_data[1] = player_name

            # Add normal rows
            length = len(team_dataframe)
            team_dataframe.loc[length] = individual_row_data

        # Adding team and year columns to the dataframe for later use in analysis
        team_dataframe['Team'] = team
        team_dataframe['Year'] = year

        # Add the cleaned data to the master list
        master_list.append(team_dataframe)

        print(f"Finished scraping data for {team} in {year}.")

# Concatenate all the individual team dataframes into a single master dataframe
master_dataframe = pd.concat(master_list, ignore_index=True)
# Save the master dataframe to a CSV file
master_dataframe.to_csv(r'C:\Users\chris\CSPN-Baseball\Test-stuff\batting_data.csv', index=False)   

print("Master dataframe created and saved to CSV file.")