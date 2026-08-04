import pandas as pd

# Saving file paths as variables to increase readability 
batting_file_path = "../data/y00-26_batting_data.csv"
pitching_file_path = "../data/y00-26_pitching_data.csv"

categories = ["player_id", "Year", "Award", "Place"]

def create_award_types(_conn):
    _cursor = _conn.cursor()

    # Creating the table values for our SQL tables 
    award_types = [
        ("AS", "All-Star"),
        ("MVP","Most Valuable Player"),
        ("CYA","Cy Young Award"),
        ("ROY","Rookie of the Year"),
        ("GG","Gold Glove"),
        ("SS","Silver Slugger"),
        ("PG","Platinum Glove")
    ]

    # Creating our award code table
    _cursor.execute("""    
        CREATE TABLE IF NOT EXISTS award_types (
            award_code TEXT PRIMARY KEY,
            award_name TEXT NOT NULL
        )
    """)

    # Filling in the table with the code and values we created & assigned to award_types
    _cursor.executemany("""
        INSERT OR REPLACE INTO award_types
        (award_code, award_name)
        VALUES (?, ?)
    """, award_types)

    _conn.commit()

def load_award_players():

    batting_file = pd.read_csv(batting_file_path)

    batting_awards = batting_file[
        batting_file["Awards"].notna()
    ]

    pitching_file = pd.read_csv(pitching_file_path)

    pitching_awards = pitching_file[
        pitching_file["Awards"].notna()
    ]

    award_players = pd.concat(
        [batting_awards, pitching_awards],
        ignore_index=True
    )

    return award_players

def build_player_awards(award_players):
    player_award_list = []
    seen = set()

    for _, player in award_players.iterrows():
        player_id = player["player_id"]
        year = player["Year"]
        awards = player["Awards"]

        print(player["Player"])
        print(player["Awards"])
        print("--------------------")

        award_list = awards.split(",")

        for award in award_list:
            award = award.strip()
            place = None
            if "-" in award:
                award_code, place = award.split("-")
                place = int(place)
            else:
                award_code = award
                place = None

            key = (
                player_id, 
                year, 
                award_code, 
                place
            )

            if key not in seen:
                seen.add(key)

                player_award_list.append([
                    player_id, 
                    year, 
                    award_code, 
                    place
                    ])

    return pd.DataFrame(player_award_list, columns=categories)

def create_awards(connection):

    create_award_types(connection)

    award_players = load_award_players()

    award_dataframe = build_player_awards(award_players)

    award_dataframe.to_sql(
        "player_awards",
        connection,
        if_exists="replace",
        index=False
    )

    connection.commit()