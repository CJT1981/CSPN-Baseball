from database.db_connection import get_connection
# from db_connection import get_connection
import pandas as pd 

# This stores my reusable SQL functions 

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

    # This accounts for user input errors, if the user inputs a stat that is not
    # in the allowed stats list, we will raise an error.
    if stat not in ALLOWED_STATS:
        raise ValueError("Invalid statistic.")

    connection = get_connection()

    # We are getting a problem with the plate appearance rule, problem being the plate
    # appearance rule is in place to eliminate non-qualified hitters to be returned for stats
    # that are rates or averages but this rule doesn't need to apply to counting stats 
    # rate stats (need PA MIN)= batting average, on base percentage, slugging percentage.
    # counting stats (don't need PA MIN) = # of homeruns, rbis, runs, hits, etc. 
    RATE_STATS = [
        'BA',
        'OBP',
        'SLG',
        'OPS',
        'OPS+',
        'rOBA',
        'Rbat+'
    ]

    if stat in RATE_STATS:
        query = f"""
            SELECT Player, Team, "{stat}" as stat_value
            FROM batting_seasons
            WHERE Year = ? 
            AND PA >= ?
            ORDER BY "{stat}" DESC
            LIMIT 50;
        """

        result_df = pd.read_sql_query(query, connection, params=(year, min_pa))
    else:
        query = f"""
            SELECT Player, Team, "{stat}" as stat_value
            FROM batting_seasons
            WHERE Year = ?
            ORDER BY "{stat}" DESC
            LIMIT 50;
        """

        result_df = pd.read_sql_query(query, connection, params=(year,))

    # We are having a problem with the ranking of the data, we are not
    # not accounting for ties in the data. Therefore, we are adding this
    # next line to adjust the ranking of the data to show ties correctly.
    # We are using the "min" method to assign the same rank to tied values,
    # and the next rank will be the next integer after the tied values.
    result_df['rank'] = result_df['stat_value'].rank(
        method='min',
        ascending=False
    )

    # We convert the rank column to an int to avoid decimal points in the
    # rank values, such as 1.0, 2.0, etc.
    result_df['rank'] = result_df['rank'].astype(int)

    connection.close()
    
    return result_df

def get_pitching_leaders(stat, year, min_ip = 162):
    """
    Returns the top players for a specified pitching statistic in a given year.

    Rate statistics such as ERA, WHIP, and FIP require a minimum number of
    innings pitched to qualify. Counting statistics such as wins, strikeouts,
    and saves do not require the minimum innings qualification.

    Parameters:
    stat (str): The pitching statistic to filter by (e.g., 'ERA', 'SO', 'WHIP').
    year (int): The year to filter the data.
    min_ip (int): The minimum number of innings pitched required for rate statistics.

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

    RATE_STATS = [
        'ERA',
        'ERA+',
        'FIP',
        'WHIP',
        'H9',
        'HR9',
        'BB9',
        'SO9',
        'W-L%',
        'SO/BB'
    ]

    ascending_stats = [
        'ERA', 
        'FIP',
        'WHIP', 
        'H9',
        'HR9',
        'BB9'
    ]

    # This accounts for user input errors, if the user inputs a stat that is not in the allowed stats list, we will raise an error.
    if stat not in ALLOWED_STATS:
        raise ValueError("Invalid statistic.")

    # This helps with the ordering of the stats, some stats are better when they are lower
    # such as ERA, WHIP, and others. And, there are others that are better when they are 
    # higher such as Wins, Strikeouts, and others. So, we need this check
    direction = 'DESC'
    if stat in ascending_stats:
        direction = 'ASC'

    connection = get_connection()

    # This allows us to apply the innings pitched qualification rule to rate stats such 
    # as ERA, WHIP, and others. But, we don't need to apply this qualifier to counting 
    # stats such as Strikouts, Wins, and others. 
    if stat in RATE_STATS:
        query = f"""
            SELECT Player, Team, "{stat}" as stat_value
            FROM pitching_seasons
            WHERE Year = ? 
            AND IP >= ?
        """
        
        result_df = pd.read_sql_query(query, connection, params=(year, min_ip))
    else:
        query = f"""
            SELECT Player, Team, "{stat}" as stat_value
            FROM pitching_seasons
            WHERE Year = ?
        """
        
        result_df = pd.read_sql_query(query, connection, params=(year,))

    # We are having a problem with some of the data coming back as strings
    # instead of floats or integers. This is causing problems with the 
    # sorting of the data. Therefore, we are adding this next line to 
    # convert the data to the correct type.
    result_df['stat_value'] = pd.to_numeric(
        result_df['stat_value'],
        errors='coerce'
    )

    # Previous version of the code was not sorting the data correctly, so instead of having 
    # it be done through SQL, we are going to have pandas do the sorting of the data. 
    result_df = result_df.sort_values(
        'stat_value',
        ascending=(direction == 'ASC')
    )

    # We are having a problem with the ranking of the data, we are not
    # not accounting for ties in the data. Therefore, we are adding this
    # next line to adjust the ranking of the data to show ties correctly.
    # We are using the "min" method to assign the same rank to tied values,
    # and the next rank will be the next integer after the tied values.
    result_df['rank'] = result_df['stat_value'].rank(
        method='min',
        ascending=(direction == 'ASC')
    )

    # We convert the rank column to an int to avoid decimal points in the
    # rank values, such as 1.0, 2.0, etc.
    result_df['rank'] = result_df['rank'].astype(int)

    # Here is where we take the top 50 players for the specified stat after it is
    # sorted and ranked correctly for us.
    result_df = result_df.head(50) 
    
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

def get_team(team_id):
    """
    parameter (str): team_id - The ID of the team to search for.
    returns: A pandas DataFrame containing the team information.
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
        WHERE team_id = ?
        ORDER BY year_id DESC;
        """

    result_df = pd.read_sql_query(query, connection, params=(team_id,))

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

def get_team_batting_leaders(year_id):
    """
    parameter (int): year_id allows us to also pair our statistics with a particular year
    return (dataframe): dataframe containing the team batting statistics per one stat
    """

    connection = get_connection()

    query = """
        SELECT *
        FROM team_batting_leaderboard
        WHERE Year = ?
    """

    result_df = pd.read_sql_query(query, connection, params=(year_id,))

    connection.close()

    return result_df