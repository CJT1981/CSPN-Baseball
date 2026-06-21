from bs4 import BeautifulSoup
import requests
import pandas as pd

# creating a list of teams and years to loop through for scraping data from multiple pages
teams = [
    "ATL", "PHI", "WSN", "MIA", "NYM", "NYY", "TBR", "TOR", "BAL", "BOS",
    "CIN", "PIT", "STL", "MIL", "CHC", "CWS", "CLE", "DET", "KC", "MIN", 
    "ARI", "COL", "LAD", "SDP", "SFG", "OAK", "SEA", "HOU", "LAA", "TEX"
    ]
# creating a list of years to loop through for scraping data from multiple pages
years = range(2000, 2027)

# looping through each team and year to scrape the data and store it in a dataframe, 
# then transfer it to a csv file
for team in teams:
    for year in years:
        print(f"Scraping data for {team} in {year}...")

        # Construct the URL for the team's batting statistics page for the given year
        url = f"https://www.baseball-reference.com/teams/{team}/{year}.shtml"
        
        html_page = requests.get(url)
        
        if html_page.status_code != 200:
            print(f"Failed to retrieve data for {team} in {year}. Status code: {html_page.status_code}")
            continue

        html_page.encoding = "utf-8" # <-- this accounts for the special char in names
        team_html = BeautifulSoup(html_page.text, "html.parser")

        # above is the table we want to scrape, but we can also find it by its id as shown below
        team_tables = team_html.find('table', id='players_standard_batting')
        # print(team_tables.prettify())

        table_titles = team_tables.find('thead').find_all('th')
        # print(table_titles)

        categories = [title.text.strip() for title in table_titles]
        # removes the duplicate 'POS' column that appears in the table
        categories.pop(-2)
        # print(categories)

        team_dataframe = pd.DataFrame(columns = categories)
        # print(team_dataframe)

        # Getting all the table data
        all_data = team_tables.find_all('tr')
        # print(all_data)

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
    # Completed Table
    print(team_dataframe)
    
    # Transfer to csv
    team_dataframe.to_csv(fr'C:\Users\chris\CSPN-Baseball\Test-stuff\{team}-batting-{year}.csv',index=False)



