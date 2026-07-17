"""
COLLECTING DATA FROM BASEBALL-REFERENCE.COM FOR PLAYER PROFILES
OBJECTIVE:
    Scrape the player unique id from baseball-reference.com for all players in the database. 
    This unique id will be used to scrape player profile data from the player profile page.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import string
import random

player_info = []
players_scraped = 0
# Adding a user-agent to the requests to avoid being blocked by the website
session = requests.Session()
session.headers.update({
    "User-Agent": 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/58.0.3029.110 Safari/537.3"
})

def get_position(meta_table):
    for p in meta_table.find_all('p'):
        if p.startswith("Position") or p.startswith("Positions"):
            if p.startswith("Positions"):
                return p.text.replace('Positions:', '').strip()
            else:
                return p.text.replace('Position:', '').strip()
    return "Unknown"  # Return Unknown if position is not found

def get_bat_and_throw(meta_table):
    for p in meta_table.find_all('p'):
        text = p.get_text(" ", strip=True)

        if 'Bats:' in text:
            bats = text.split('Bats:')[1].split('Throws:')[0].strip()
            throws = text.split('Throws:')[1].strip()
            return bats, throws
    return "Unknown", "Unknown"  # Return Unknown if bats and throws are not found

def get_height_and_weight(meta_table):
    for p in meta_table.find_all('p'):
        spans = p.find_all('span')
        if len(spans) >= 2:
            if "lb" in spans[1].text:
                height = spans[0].text.strip()
                weight = spans[1].text.strip()
                return height, weight
    return "Unknown", "Unknown"  # Return Unknown if height and weight are not found

def get_debut_and_last_game(meta_table):
    _debut, _last_game = None, None
    for p in meta_table.find_all('p'):
        if 'Debut:' in p.text:
            _debut = p.text.replace('Debut:', '').strip()
        if 'Last Game:' in p.text:
            _last_game = p.text.replace('Last Game:', '').strip()
    return _debut, _last_game

for letter in string.ascii_lowercase:
    # Constructing the URL for every letter of the alphabet to scrape player data
    url = f"https://www.baseball-reference.com/players/{letter}/"

    try:
        html_page = session.get(url, timeout=20)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to retrieve data for {letter} page: {e}")
        continue

    # Adding a delay between requests to avoid overwhelming the server
    time.sleep(random.uniform(2.5, 5))  # Random delay between 2.5 and 5 seconds

    # Check if the request was successful
    if html_page.status_code != 200:
        print(f"Failed to retrieve data for {letter} page. Status code: {html_page.status_code}")
        continue

    html_page.encoding = "utf-8" # <-- this accounts for the special char in names
    letter_html = BeautifulSoup(html_page.text, "html.parser")
    
    # Finding the div that contains the player list
    # This corresponds to <div class="section_content" id="div_players_">
    player_section = letter_html.find('div', id='div_players_')

    # Finding every player in the section and storing them in player rows
    player_rows = player_section.find_all('p')

    for player in player_rows:
        # Pulling the link to the player profile page from the <a> tag
        link = player.find('a')

        # if the link doesn't exist, skip to the next iteration
        # This allows us to skip any unexpected HTML 
        if link is None:
            continue

        # Pulling the players name, example: Henry Aaron
        player_name = link.text.strip()

        # Pulling the player URL, example: /players/a/aaronha01.shtml
        player_url = link['href']

        # Pulling the baseball reference ID, example: aaronha01
        # 1. splitting the url by '/'
        # 2. taking the last element of the list, which holds the ID
        # 3. removing the '.shtml' from the end of the ID
        bbref_id = player_url.split('/')[-1].replace('.shtml', '')

        # Scrape the player profile page to get additional information
        # Building the full URL to the player profile page
        profile_url = f"https://www.baseball-reference.com{player_url}"

        success = False

        for attempt in range(3):  # Retry up to 3 times
            try:
                html_profilepage = session.get(profile_url, timeout=20)
                success = True
                break  # Exit the retry loop if successful
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}: An error occurred while trying to retrieve profile data for {player_name}: {e}")
                time.sleep(5)  # Wait before retrying

        # Adding a delay between requests to avoid overwhelming the server
        time.sleep(random.uniform(2.5, 5))  # Random delay between 2.5 and 5 seconds

        html_profilepage.encoding = "utf-8" # <-- this accounts for the special char in names
        player_profile_html = BeautifulSoup(html_profilepage.text, "html.parser")

        # The data we want is in a table with an id of 'meta'
        meta_table = player_profile_html.find('div', id='meta')
        
        # Extracting the birth date, birth place, height, and weight from the meta table
        # They are stored in <p> tags, so we can find all <p> tags and extract the relevant information
        # To clean up a little bit, I created from helper functions
        position = get_position(meta_table)
        bats, throws = get_bat_and_throw(meta_table) 
        height, weight = get_height_and_weight(meta_table)
        debut, last_game = get_debut_and_last_game(meta_table)
        # Pulling the player's birthdate
        birth_span = meta_table.find('span', id='necro-birth')
        if birth_span:
            birth_date = birth_span['data-birth']
        else:
            birth_date = None

        # Storing our data into a 'player' dictionary
        player_info.append(
            {
                "player_id": bbref_id,
                "player_name": player_name,
                "position": position,
                "bats": bats,
                "throws": throws,
                "height": height,
                "weight": weight,
                "birth_date": birth_date,
                "debut": debut,
                "last_game": last_game
            }
        )
        players_scraped += 1
        print(f"{players_scraped}: {player_name} profile scraped successfully.")

        if len(player_info) % 100 == 0:
            pd.DataFrame(player_info).to_csv(
                "player_profile_progress.csv",
                index=False
                )
            print(f"Scraped {len(player_info)} players so far...")
        
player_profile_df = pd.DataFrame(player_info)
player_profile_df.to_csv(r'C:\Users\chris\CSPN-Baseball\data\player_profiles.csv', index=False)
print("Finished scraping player profiles. Data saved to 'player_profiles.csv'.")


"""
    IN ORDER TO GET THE UNIQUE PLAYER ID, WE NEED TO SCRAPE 
    THIS TABLE FROM THE PLAYER BY ALPHABETICAL LETTER PAGE:
    <div class="section_content" id="div_players_">
	    <p><a href="/players/a/aardsda01.shtml">David Aardsma</a>  (2004-2015)</p>
        <p><a href="/players/a/aaronha01.shtml">Henry Aaron</a>+ (1954-1976)</p> ...
        <p><a href="/players/a/azcuejo01.shtml">Joe Azcue</a>  (1960-1972)</p>
        <p><b><a href="/players/a/azocajo01.shtml">José Azócar</a>  (2022-2026)</b></p>
        <p><a href="/players/a/azocaos01.shtml">Oscar Azócar</a>  (1990-1992)</p>		
    </div>


    IN ORDER TO GET PLAYER INFO SUCH AS BIRTH DATE, BIRTH PLACE, 
    HEIGHT, WEIGHT, ETC. WE NEED TO SCRAPE THEIR PROFILE PAGE, WHICH WE CAN
    ACCESS USING THE PLAYER URL WE SCRAPED FROM THE TABLE ABOVE.
    <div>
	<h1>
		<span>David Aardsma</span>
    </h1>
        
    <p>
        <strong>Position:</strong>
        Pitcher
    </p>

    <p>
        <strong>Bats: </strong>Right
            &nbsp;•&nbsp;
        <strong>Throws: </strong>Right
    </p>

    <p><span>6-3</span>,&nbsp;<span>215lb</span>&nbsp;(190cm,&nbsp;97kg) </p>

    <p>
    <strong><a href="/bio/">Born:</a></strong>
        <span id="necro-birth" data-birth="1981-12-27">
        <a href="/friv/birthdays.cgi?month=12&amp;day=27">December 27</a>, <a href="/leagues/majors/1981-births.shtml">1981</a>
        </span> <span><nobr>(Age:&nbsp;44-194d)</nobr></span> ...
</div>
"""