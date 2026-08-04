import pandas as pd

franchise_file_path = "../data/franchise_history.csv"

def create_franchise(_conn):
    _cursor = _conn.cursor()

    teams = [
        ('ARI','Diamondbacks'),
        ('OAK','Athletics'),
        ('ATL','Braves'),
        ('BAL','Orioles'),
        ('BOS','Red Sox'),
        ('CHC','Cubs'),
        ('CHW','White Sox'),
        ('CIN','Reds'),
        ('CLE','Guardians'),
        ('COL','Rockies'),
        ('DET','Tigers'),
        ('HOU','Astros'),
        ('KCR','Royals'),
        ('ANA','Angels'),
        ('LAD','Dodgers'),
        ('FLA','Marlins'),
        ('MIL','Brewers'),
        ('MIN','Twins'),
        ('NYM','Mets'),
        ('NYY','Yankees'),
        ('PHI','Phillies'),
        ('PIT','Pirates'),
        ('SDP','Padres'),
        ('SFG','Giants'),
        ('SEA','Mariners'),
        ('STL','Cardinals'),
        ('TBD','Rays'),
        ('TEX','Rangers'),
        ('TOR','Blue Jays'),
        ('WSN','Nationals')
    ]

    _cursor.execute("""
        CREATE TABLE IF NOT EXISTS franchises (
            franchise_id TEXT PRIMARY KEY,
            franchise_name TEXT
        )
    """)

    _cursor.executemany("""
        INSERT OR REPLACE INTO franchises
        (franchise_id, franchise_name)
        VALUES (?,?)
    """, teams)

    _conn.commit()

def create_team_seasons(_conn):

    create_franchise(_conn)

    franchise_dataframe = pd.read_csv(franchise_file_path)

    franchise_dataframe.to_sql(
        'franchise_history',
        _conn,
        if_exists='replace',
        index=False
    )

    _conn.commit()