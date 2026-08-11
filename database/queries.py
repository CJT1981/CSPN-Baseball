from database.db_connection import get_connection
# from db_connection import get_connection
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

def get_player_profile(player_id):
    """
    Parameter (str): player_id - The unique identifier for the player.
    Returns: A pandas DataFrame containing the player's profile information.
    """

    connection = get_connection()
    
    query = """
        SELECT *
        FROM player_profiles
        WHERE player_id = ?
    """
    
    result_df = pd.read_sql_query(query, connection, params=(player_id,))
    
    connection.close()
    
    return result_df

def get_player_career_batting(player_id):
    """
    Parameter (str): player_id - The unique identifier for the player.
    Returns: A pandas DataFrame containing the player's career batting statistics.
    """

    connection = get_connection()
    
    query = """
        SELECT *
        FROM career_batting
        WHERE player_id = ?
    """
    
    result_df = pd.read_sql_query(query, connection, params=(player_id,))
    
    connection.close()
    
    return result_df

def get_player_career_pitching(player_id):
    """
    Parameter (str): player_id - The unique identifier for the player.
    Returns: A pandas DataFrame containing the player's career pitching statistics.
    """

    connection = get_connection()
    
    query = """
        SELECT *
        FROM career_pitching
        WHERE player_id = ?
    """
    
    result_df = pd.read_sql_query(query, connection, params=(player_id,))
    
    connection.close()
    
    return result_df

def get_batting_seasons(player_id):
    """
    Parameter (str): player_id - The unique identifier for the player.
    Returns: A pandas DataFrame containing the player's batting seasons.
    """

    connection = get_connection()
    
    query = """
        SELECT *
        FROM batting_seasons
        WHERE player_id = ?
        ORDER BY Year;
    """
    
    result_df = pd.read_sql_query(query, connection, params=(player_id,))
    
    connection.close()
    
    return result_df

def get_pitching_seasons(player_id):
    """
    Parameter (str): player_id - The unique identifier for the player.
    Returns: A pandas DataFrame containing the player's pitching seasons.
    """

    connection = get_connection()
    
    query = """
        SELECT *
        FROM pitching_seasons
        WHERE player_id = ?
        ORDER BY Year;
    """
    
    result_df = pd.read_sql_query(query, connection, params=(player_id,))
    
    connection.close()
    
    return result_df

def get_batting_leaders(stat, year, min_pa = 502):
    """
    Returns the top players for a specified batting statistic in a given year among players with the 
    qualified number of plate appearances.

    Parameters:
    stat (str): The batting statistic to filter by (e.g., 'BA', 'HR', 'OPS').
    year (int): The year to filter the data.
    min_pa (int): 502 - The minimum number of plate appearances to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top players for the specified statistic.
    """

    
    ALLOWED_STATS = [
        'WAR',
        'G',
        'PA',
        'AB',
        'R',
        'H',
        '2B',
        '3B',
        'HR',
        'RBI',
        'SB',
        'CS',
        'BB',
        'SO',
        'BA',
        'OBP',
        'SLG',
        'OPS',
        'OPS+',
        'rOBA',
        'Rbat+',
        'TB',
        'GIDP',
        'HBP',
        'SH',
        'SF',
        'IBB'
    ]

    # This accounts for user input errors, if the user inputs a stat that is not in the allowed stats list, we will raise an error.
    if stat not in ALLOWED_STATS:
        raise ValueError("Invalid statistic.")

    connection = get_connection()
    
    query = f"""
        SELECT Player, Team, {stat} as stat_value
        FROM batting_seasons
        WHERE Year = ? 
        AND PA >= ?
        ORDER BY {stat} DESC
        LIMIT 50;
    """
    
    result_df = pd.read_sql_query(query, connection, params=(year, min_pa))
    connection.close()
    
    return result_df

def get_pitching_leaders(stat, year, min_ip = 162):
    """
    Returns the top players for a specified pitching statistic in a given year among players with the 
    qualified number of innings pitched.

    Parameters:
    stat (str): The pitching statistic to filter by (e.g., 'ERA', 'SO', 'WHIP').
    year (int): The year to filter the data.
    min_ip (int): 162 - The minimum number of innings pitched to consider.
    
    Returns:
    DataFrame: A pandas DataFrame containing the top players for the specified statistic.
    """

    ALLOWED_STATS = [
        'WAR',
        'W',
        'L',
        'W-L%',
        'ERA',
        'G',
        'GS',
        'GF',
        'CG',
        'SHO',
        'SV',
        'IP',
        'H',
        'R',
        'ER',
        'HR',
        'BB',
        'IBB',
        'SO',
        'HBP',
        'BK',
        'WP',
        'BF',
        'ERA+',
        'FIP',
        'WHIP',
        'H9',
        'HR9',
        'BB9',
        'SO9',
        'SO/BB'
    ]

    ascending_stats = [
        'ERA', 
        'H',
        'R',
        'ER',
        'HR',
        'BB',
        'WHIP', 
        'H9',
        'HR9',
        'BB9'
    ]

    # This accounts for user input errors, if the user inputs a stat that is not in the allowed stats list, we will raise an error.
    if stat not in ALLOWED_STATS:
        raise ValueError("Invalid statistic.")

    direction = 'DESC'
    if stat in ascending_stats:
        direction = 'ASC'

    connection = get_connection()
    
    query = f"""
        SELECT Player, Team, [{stat}] as stat_value
        FROM pitching_seasons
        WHERE Year = ? 
        AND IP >= ?
        ORDER BY [{stat}] {direction}
        LIMIT 50;
    """
    
    result_df = pd.read_sql_query(query, connection, params=(year, min_ip))
    
    connection.close()
    
    return result_df

def get_player_search(user_input):
    """
    parameter (str): user_input - The input string to search for in player names.
    returns: A pandas DataFrame containing the players that match the search criteria.
    """

    connection = get_connection()

    query = """
        SELECT
            player_id,
            player_name
        FROM player_bio
        WHERE player_name LIKE ?
        ORDER BY player_name;
        """

    result_df = pd.read_sql_query(query, connection, params=(user_input))

    connection.close()

    return result_df

def get_team(team_id, year_id):
    """
    parameter (str): team_id - The ID of the team to search for.
    parameter (int): year_id - The year to filter the data.
    returns: A pandas DataFrame containing the team information for the specified year.
    """

    connection = get_connection()

    query = """
        SELECT 
            year_id,
            team_name,
            league,
            division,
            number_of_games,
            wins,
            losses,
            ties,
            winning_percentage,
            finish,
            playoff_result
        FROM franchise_history
        WHERE team_id = ? AND year_id = ?;
        """

    result_df = pd.read_sql_query(query, connection, params=(team_id, year_id))

    connection.close()

    return result_df

def get_team_roster(team_id, year_id):
    """
    parameter (str): team_id - The ID of the team to search for.
    parameter (int): year_id - The year to filter the data.
    returns: A pandas DataFrame containing the team roster for the specified year.
    """

    connection = get_connection()

    query = """
        SELECT 
            player_id,
            Player,
            Pos,
            G
        FROM batting_seasons
        WHERE Team = ? AND Year = ?;
        """

    batting_team_df = pd.read_sql_query(query, connection, params=(team_id, year_id))

    query = """
        SELECT
            player_id,
            Player,
            Pos,
            G
        FROM pitching_seasons
        WHERE Team = ? AND Year = ?;
    """

    pitching_team_df = pd.read_sql_query(query, connection, params=(team_id, year_id))

    connection.close()

    return batting_team_df, pitching_team_df