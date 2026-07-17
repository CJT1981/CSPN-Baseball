from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random

def get_position(meta_table):

    for p in meta_table.find_all("p"):

        text = p.get_text(" ", strip=True)

        if text.startswith("Position:") or text.startswith("Positions:"):

            text = text.replace("Position:", "")
            text = text.replace("Positions:", "")

            return text.strip()

    return "Unknown"

player_file = pd.read_csv("../data/player_profiles.csv")

unknown_players = player_file[
    player_file["position"].isna() | (
    player_file['position'] == 'Unknown')
    ]

print(f"Number of players with unknown positions: {len(unknown_players)}")

session = requests.Session()

session.headers.update({
    "User-Agent": 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/58.0.3029.110 Safari/537.3"
})

for index, row in unknown_players.iterrows():
    player_id = row["player_id"]
    profile_url = (
        f"https://www.baseball-reference.com/players/{player_id[0]}/{player_id}.shtml"
    )

    player_html_page = session.get(profile_url)
    """
    print(profile_url)
    print(player_html_page.status_code)
    print(player_html_page.url)
    print(player_html_page.text[:500])
    break
    """
    time.sleep(random.uniform(3,6))
    player_page = BeautifulSoup(player_html_page.text, "html.parser")

    meta = player_page.find("div", id="meta")
    
    if meta is None:
        print(f"Meta information not found for {row['player_name']}. Skipping...")
        continue

    position = get_position(meta)

    player_file.loc[index, "position"] = position

    print(f"Updated position for {row['player_name']}: {position}")

player_file.to_csv("../data/final_player_profiles.csv", index=False)