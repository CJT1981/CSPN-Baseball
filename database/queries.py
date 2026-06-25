from db_connection import get_connection
import pandas as pd 

# This stores my reusable SQL functions 

def top_batting_average(year, min_at_bats = 502):
    """
    Returns the top batting averages for a given year among players with the 
    qualified number of at-bats.

    MLB rules state that a player must have 3.1 plate appearances per league game to qualify
    for any leaderboard. In a 162-game season, this equates to 502 plate appearances.
    
    Parameters:
    year (int): The year to filter the data.
    min_at_bats (int): 502 - The minimum number of at-bats to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top batting averages.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Player, Team, BA as batting_average
        FROM batting_statistics
        WHERE Year = {year} 
        AND AB >= {min_at_bats}
        ORDER BY batting_average DESC
        LIMIT 10;
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df