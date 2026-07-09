from db_connection import get_connection
import pandas as pd 

# This stores my reusable SQL functions 

def top_batting_average(year, min_pa = 502):
    """
    Returns the top batting averages for a given year among players with the 
    qualified number of at-bats.

    MLB rules state that a player must have 3.1 plate appearances per league game to qualify
    for any leaderboard. In a 162-game season, this equates to 502 plate appearances.
    
    Parameters:
    year (int): The year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top batting averages.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Player, Team, BA as batting_average
        FROM batting_statistics
        WHERE Year = {year} 
        AND PA >= {min_pa}
        ORDER BY batting_average DESC
        LIMIT 10;
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df

def top_home_runs(year, min_pa = 502):
    """
    Returns the top home run hitters for a given year among players with the 
    qualified number of plate appearances.

    Parameters:
    year (int): The year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top home run hitters.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Player, Team, HR as home_runs
        FROM batting_statistics
        WHERE Year = {year} 
        AND PA >= {min_pa}
        ORDER BY home_runs DESC
        LIMIT 10;
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df

def team_HR_leaders(year, min_pa = 502):
    """
    Returns the top home run hitters for each team in a given year, we do not need a 
    plate qualify because HR is a counting stat that is not affected by plate appearances. 
    However, we will still include the min_pa parameter for consistency.

    Parameters:
    year (int): The year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top home run hitters by team.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Team, Player, HR as home_runs
        FROM batting_statistics
        WHERE Year = {year} 
        AND HR = (
            SELECT MAX(HR) 
            FROM batting_statistics AS HR_leaders
            WHERE HR_leaders.Team = batting_statistics.Team 
            AND HR_leaders.Year = {year} 
        )
        GROUP BY Team;
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df

def best_OPS_per_season(start_year, end_year, min_pa = 502):
    """
    Returns the best OPS (On-base Plus Slugging) seasons for players between the specified 
    years.

    Parameters:
    start_year (int): The starting year to filter the data.
    end_year (int): The ending year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the best OPS seasons.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Player, Year, Team, OPS
        FROM batting_statistics
        WHERE Year BETWEEN {start_year} AND {end_year}
        AND PA >= {min_pa}
        AND OPS = (
            SELECT MAX(OPS) 
            FROM batting_statistics AS OPS_leaders
            WHERE OPS_leaders.Year = batting_statistics.Year
            AND OPS_leaders.PA >= {min_pa}
        )
        ORDER BY Year
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df

def best_OPS_seasons(start_year, end_year, min_pa = 502):
    """
    Returns the best OPS (On-base Plus Slugging) seasons for players between the specified 
    years.

    Parameters:
    start_year (int): The starting year to filter the data.
    end_year (int): The ending year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the best OPS seasons.
    """
    connection = get_connection()
    
    query = f"""
        SELECT Player, Year, Team, OPS
        FROM batting_statistics
        WHERE Year BETWEEN {start_year} AND {end_year}
        AND PA >= {min_pa}
        ORDER BY OPS DESC
        LIMIT 25;
    """
    
    result_df = pd.read_sql_query(query, connection)
    
    connection.close()
    
    return result_df