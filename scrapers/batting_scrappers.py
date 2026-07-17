from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# creating a list of teams and years to loop through for scraping data from multiple pages
teams = [
    "ATL", "PHI", "WSN", "MIA", "NYM", "NYY", "TBR", "TOR", "BAL", "BOS",
    "CIN", "PIT", "STL", "MIL", "CHC", "CHW", "CLE", "DET", "KC", "MIN", 
    "ARI", "COL", "LAD", "SDP", "SFG", "OAK", "SEA", "HOU", "LAA", "TEX"
    ]
# creating a list of years to loop through for scraping data from multiple pages
years = range(2000, 2027)

master_list = []
# looping through each team and year to scrape the data and store it in a dataframe, 
# then transfer it to a csv file
for year in years:
    for team in teams:

        url_team = team
        # fixing error with team abbreviations for OAK
        if team == "OAK" and year >= 2025:
            url_team = "ATH"
        if team == "LAA" and year <= 2004:
            url_team = "ANA"
        if team == "TBR" and year <= 2007:
            url_team = "TBD"
        if team == "WSN" and year <= 2004:
            url_team = "MON"

        print(f"Scraping data for {url_team} in {year}...")

        # Construct the URL for the team's batting statistics page for the given year
        url = f"https://www.baseball-reference.com/teams/{url_team}/{year}.shtml"
        
        html_page = requests.get(url)

        # Adding a delay between requests to avoid overwhelming the server
        time.sleep(3)
        
        # Check if the request was successful
        if html_page.status_code != 200:
            print(f"Failed to retrieve data for {url_team} in {year}. Status code: {html_page.status_code}")
            continue

        html_page.encoding = "utf-8" # <-- this accounts for the special char in names
        team_html = BeautifulSoup(html_page.text, "html.parser")

        team_tables = team_html.find('table', id='players_standard_batting')

        # If the table is not found, skip to the next iteration
        if team_tables is None:
            print(f"No batting data found for {url_team} in {year}. Skipping...")
            continue

        table_titles = team_tables.find('thead').find_all('th')

        categories = [title.text.strip() for title in table_titles]

        # removes Rk column that appears in the table
        categories.pop(0)

        # removes the duplicate 'POS' column that appears in the table
        categories.pop(-2)

        categories.insert(0, 'player_id')  # Insert 'player_id' at the beginning of the categories list

        team_dataframe = pd.DataFrame(columns = categories)

        # Getting all the table data
        all_data = team_tables.find_all('tr')

        # Cleaning the data
        for each_row in all_data:
            player_id = None
            row_header = each_row.find('th')

            if row_header is None:
                continue

            row_data = each_row.find_all('td')

            individual_row_data = [data.text.strip() for data in row_data]

            # Skip empty rows
            if len(individual_row_data) == 0:
                continue

            # To remove pitcher names from coming up in the batting data, we can skip
            # over any rows that include "P" in the position column (Pos)
            # Find the position column
            pos_index = categories.index('Pos')
            # print(f"Position index: {pos_index}, Position value: {individual_row_data[pos_index-1]}")  # Debugging line
            # Skip pitchers
            if individual_row_data[pos_index-1] == 'P':
                continue
            
            # removes the values in the duplicate 'POS' column that appears in the table
            individual_row_data.pop(-2)
            
            # Skip repeated header rows
            if row_header.text.strip() == 'Rk':
                continue

            # Remove team totals from data
            player_name = individual_row_data[0]

            if player_name in [
                'Team Totals',
                'Pitcher Totals',
                'Non-Pitcher Totals'
            ]:
                continue

            player_cell = each_row.find('td', {'data-stat': 'name_display'})
            if player_cell: 
                player_id = player_cell.get('data-append-csv')

            # Clean player names
            player_name = player_name.replace("*", "")
            player_name = player_name.replace("#", "")

            # Remove anything inside parentheses
            player_name = player_name.split("(")[0].strip()

            individual_row_data[0] = player_name

            # print(individual_row_data)
            # Add normal rows
            length = len(team_dataframe)
            individual_row_data.insert(0, player_id)  # Insert player_id at the beginning of the row
            team_dataframe.loc[length] = individual_row_data

        # Adding team and year columns to the dataframe for later use in analysis
        team_dataframe['Team'] = team
        team_dataframe['Year'] = year

        # Reorder the columns to have 'Team' and 'Year' at the front
        columns = team_dataframe.columns.tolist()

        new_order = ['player_id', 'Team', 'Year'] + [
            col for col in columns 
            if col not in ['player_id', 'Team', 'Year']
        ]

        team_dataframe = team_dataframe[new_order]

        # Add the cleaned data to the master list
        master_list.append(team_dataframe)

        print(f"Finished scraping data for {url_team} in {year}.")

# Concatenate all the individual team dataframes into a single master dataframe
master_dataframe = pd.concat(master_list, ignore_index=True)
# Save the master dataframe to a CSV file
master_dataframe.to_csv(r'C:\Users\chris\CSPN-Baseball\data\y00-26_batting_data.csv', index=False)   

print("Master dataframe created and saved to CSV file.")