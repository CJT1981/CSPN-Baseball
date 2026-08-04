from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import random

teams = [
    "ATL", "PHI", "WSN", "FLA", "NYM", "NYY", "TBD", "TOR", "BAL", "BOS",
    "CIN", "PIT", "STL", "MIL", "CHC", "CHW", "CLE", "DET", "KCR", "MIN", 
    "ARI", "COL", "LAD", "SDP", "SFG", "OAK", "SEA", "HOU", "ANA", "TEX"
    ]

team_seasons = []

for team in teams:
    url = f"https://www.baseball-reference.com/teams/{team}/"
    
    print(f"Scraping data for {team} ...")

    html_page = requests.get(url)

    if html_page.status_code != 200:
        print(f"Failed to retrieve data for {team}. Status code: {html_page.status_code}")
        continue

    time.sleep(random.uniform(2.5,5))

    franchise_html = BeautifulSoup(html_page.text, "html.parser")

    franchise_table = franchise_html.find('table', id='franchise_years')

    rows = franchise_table.find("tbody").find_all('tr')

    for row in rows:
        division = None
        # To account for separator rows, we check and skip it
        if row.get('class') == ['thead']:
            continue

        year_cell = row.find('th', {"data-stat": 'year_ID'})
        year = year_cell.text.strip()
        href = year_cell.find('a')["href"]
        team_id = href.split('/')[2]
        team_name = row.find('td', {"data-stat": 'team_name'}).text.strip()
        league = row.find('td', {"data-stat": 'lg_ID'}).text.strip()
        if ' ' in league:
            league, division = league.split(' ')
        number_of_games = row.find('td', {"data-stat": 'G'}).text.strip()
        wins = row.find('td', {"data-stat": 'W'}).text.strip()
        losses = row.find('td', {"data-stat": 'L'}).text.strip()
        ties = row.find('td', {"data-stat": 'ties'}).text.strip()
        winning_percentage = row.find('td', {"data-stat": 'win_loss_perc'}).text.strip()
        finish = row.find('td', {"data-stat": 'finish'}).text.strip()
        playoff_result = row.find('td', {"data-stat": 'playoffs'}).text.strip()

        team_seasons.append({
            "franchise_id": team,
            "team_id": team_id,
            "year_id": year,
            "team_name": team_name,
            "league": league,
            "division": division,
            "number_of_games": number_of_games,
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "winning_percentage": winning_percentage,
            "finish": finish,
            "playoff_result": playoff_result
        })

    print(f"Finished scraping data for {team}.")
    print("--------------------")

franchise_history_df = pd.DataFrame(team_seasons)
franchise_history_df.to_csv('../data/franchise_history.csv', index=False)
print("Finished scraping franchise history. Data saved to 'franchise_history.csv'.")


