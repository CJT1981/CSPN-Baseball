import pandas as pd
import sqlite3
from db_connection import get_connection
from create_awards import create_awards
from create_teams import create_team_seasons

def main():
    # Load my csv data
    dframe = pd.read_csv('../data/y00-26_batting_data.csv')

    # Connect to SQLite database
    connection = get_connection()

    # Write the DataFrame to a SQL table named 'batting_statistics'
    dframe.to_sql(
        'batting_statistics', 
        connection, if_exists='replace', 
        index=False
    )

    dframe = pd.read_csv('../data/final_player_profiles.csv')

    dframe.to_sql(
        'player_profiles', 
        connection, if_exists='replace', 
        index=False
    )

    dframe = pd.read_csv('../data/y00-26_pitching_data.csv')

    dframe.to_sql(
        'pitching_statistics',
        connection, if_exists="replace",
        index=False
    )

    create_awards(connection)
    create_team_seasons(connection)

    connection.close()

    print("Database created successfully and data inserted into 'batting_statistics' table.")

if __name__ == "__main__":
    main()