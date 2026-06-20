from bs4 import BeautifulSoup
import requests
import pandas as pd

# creating a list of teams and years to loop through for scraping data from multiple pages
teams = [
    "ATL", "NYY", "BOS"
    ]
year = "2026"


for team in teams:

    url = f"https://www.baseball-reference.com/teams/{team}/{year}.shtml"
    html_page = requests.get(url)
    html_page.encoding = "utf-8" # <-- this accounts for the special char in names
    team_html = BeautifulSoup(html_page.text, "html.parser")
    '''
    <table class="stats_table sortable soc now_sortable sticky_table eq2 re2 le2" 
    id="players_standard_batting" data-cols-to-freeze=",2" data-soc-sum-scope-type="player_season" 
    data-soc-sum-phase-type="reg" data-soc-sum-table-type="Batting::BattingStandard" 
    data-soc-sum-params="null" data-soc-sum-year="2025">…</table>
    '''
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



