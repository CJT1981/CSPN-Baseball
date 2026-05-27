from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.baseball-reference.com/teams/ATL/2026.shtml"
html_page = requests.get(url)
html_page.encoding = "utf-8" # <-- this accounts for the special char in names
team_html = BeautifulSoup(html_page.text, "html.parser")

team_tables = team_html.find_all('table')[10]
# print(team_tables.prettify())

# The below line is flawed because this line of code includes repeated headers. We 
# only want to return unique headers therefore the line below the next fixes this
# table_titles = team_tables.find_all('th')
table_titles = team_tables.find('thead').find_all('th')
# print(table_titles)

# Cleaning up the table headers
categories = [title.text.strip() for title in table_titles]
# print(categories)

# Creating the data frame using the table headers (categories) as the columns
team_dataframe = pd.DataFrame(columns = categories)
# print(team_dataframe)

# Getting all the table data
all_data = team_tables.find_all('tr')
# print(all_data)

# Cleaning the data
for each_row in all_data:
    row_header = each_row.find('th')
    row_data = each_row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]

    # Skip empty rows
    if len(individual_row_data) == 0:
        continue
    
    rank = row_header.text.strip()
    individual_row_data.insert(0, rank)

    # Clean player names
    player_name = individual_row_data[1]

    player_name = player_name.replace("*", "")
    player_name = player_name.replace("#", "")

    # Remove anything inside parentheses
    player_name = player_name.split("(")[0].strip()

    individual_row_data[1] = player_name

    # Stop after Luke Williams
    if "Luke Williams" in individual_row_data:
        length = len(team_dataframe)
        team_dataframe.loc[length] = individual_row_data
        break

    # Add normal rows
    length = len(team_dataframe)
    team_dataframe.loc[length] = individual_row_data

# Completed Table
print(team_dataframe)

# Transfer to csv
team_dataframe.to_csv(r'C:\Users\chris\CSPN-Baseball\atlanta-braves-test2',index=False)