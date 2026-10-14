from flask import Flask, render_template, request
from database.queries import *

app = Flask(__name__)

@app.route('/')
def home():
    # 1st Iteration
    search_query = request.args.get('search', '').strip()

    players = None
    search_performed = False

    if search_query:
        players = get_player_search(search_query)
        search_performed = True

    return render_template(
        'home.html',
        players=players,
        search_query=search_query,
        search_performed=search_performed
    )

# Creating a route for the player profile page
@app.route('/player/<player_id>')
def player_profile(player_id):
    # TEST #6:
    # We need to account for players like Shohei Ohtani, where they have both batting 
    # and pitching statistics. We need to be able to pull both data sets.


    # GET PLAYER PROFILE
    profile_data = get_player_profile(player_id)

    # If there is no profile data, return a 404 error page
    if profile_data.empty:
        return "Player not found", 404

    # DETERMINE IF PLAYER IS A PITCHER OR NON-PITCHER
    profile = profile_data.iloc[0].to_dict()

    pitching_career_stats = get_player_career_pitching(player_id)
    pitching_season_stats = get_pitching_seasons(player_id)

    batting_career_stats = get_player_career_batting(player_id)
    batting_season_stats = get_batting_seasons(player_id)

    has_batting_stats = (
        not batting_career_stats.empty or not batting_season_stats.empty
    )

    has_pitching_stats = (
        not pitching_career_stats.empty or not pitching_season_stats.empty
    )

    """
    # Converting the Dataframes into dictionaries
    player_career_stats = player_career_stats.to_dict('records')
    player_career_stats = player_season_stats.to_dict('records')
    """
    # SEND OUR DATA TO HTML
    return render_template(
        "player_profile.html",
        profile=profile,
        batting_season_stats=batting_season_stats,
        batting_career_stats=batting_career_stats,
        pitching_season_stats=pitching_season_stats,
        pitching_career_stats=pitching_career_stats,
        has_batting_stats=has_batting_stats,
        has_pitching_stats=has_pitching_stats
    )

@app.route('/leaderboard/batting/<int:year>')
def batting_leaderboard(year):
    # 6th Iteration
    
    # We have a function to get the leaderboard for the stat we want, we
    # just need to get these individual stat leaders. We will get this 
    # done here:
    
    # We are working with this dictionary, so we can have a more 
    # descriptive understanding of our data rather than an array or list
    STATS = {
        'WAR' : 'Wins Above Replacement',
        'G' : 'Games Played',
        'PA' : 'Plate Appearances',
        'AB' : 'At Bats',
        'R' : 'Runs Scored',
        'H' : 'Hits',
        '2B' : 'Doubles',
        '3B' : 'Triples',
        'HR' : 'Home Runs',
        'RBI' : 'Runs Batted In',
        'SB' : 'Stolen Bases',
        'CS' : 'Caught Stealing',
        'BB' : 'Walks',
        'SO' : 'Strikeouts',
        'BA' : 'Batting Average',
        'OBP' : 'On Base Percentage',
        'SLG' : 'Slugging Percentage',
        'OPS' : 'On Base + Slugging Percentage',
        'OPS+' : 'OPS+',
        'rOBA' : 'rOBA',
        'Rbat+' : 'Rbat+',
        'TB' : 'Total Bases',
        'GIDP' : 'Grounded Into Double Plays',
        'HBP' : 'Hit By Pitches',
        'SH' : 'Sacrifice Hits',
        'SF' : 'Sacrifice Flys',
        'IBB' : 'Intential Walks'
    }
    
    leaderboards = {}
    
    for stat, name in STATS.items():
        leaderboards[stat] = {
            'name': name,
            'data': get_batting_leaders(stat,year)
        }
    """
    print(leaderboards['BA']['data'])
    """ 
    return render_template(
        'batting_leaderboard.html',
        year = year,
        leaderboards = leaderboards
    )

@app.route('/leaderboard/pitching/<int:year>')
def pitching_leaderboard(year):
    # 5th iteration
    
    # Similar to the batting leaderboard we are going to pull data via 
    # dataframes and we are going to save it through a dictionary and 
    # we are going to pass it to the template to be rendered.
    
    # The stats we are going to show leaderboards for 
    STAT = {
        'WAR' : 'Wins Above Replacement',
        'W' : 'Wins',
        'L' : 'Losses',
        'ERA' : 'Earned Run Average',
        'G' : 'Games Pitched',
        'GS' : 'Games Started',
        'CG' : 'Complete Games',
        'SHO' : 'Shutouts',
        'SV' : 'Saves',
        'IP' : 'Innings Pitched',
        'H' : 'Hits Allowed',
        'R' : 'Runs Allowed',
        'ER' : 'Earned Runs Allowed',
        'HR' : 'Homeruns Allowed',
        'BB' : 'Walks allowed',
        'SO' : 'Strikeouts',
        'HBP' : 'Hit By Pitches',
        'ERA+' : 'Earned Run Average Plus',
        'FIP' : 'Fielding Independent Pitching',
        'WHIP' : 'Walks plus Hits per Inning Pitched',
        'H9' : 'Hits per 9',
        'HR9' : 'Homeruns per 9',
        'BB9' : 'Walks per 9',
        'SO9' : 'Strikeouts per 9',
        'SO/BB' : 'Strikeouts per Walk'
    }
    
    leaderboards = {}
    
    for stat, name in STAT.items():
        # print(get_pitching_leaders(stat,year).dtypes)

        leaderboards[stat] = {
            'name' : name,
            'data' : get_pitching_leaders(stat,year)
        }
    
    return render_template(
        'pitching_leaderboard.html',
        year=year,
        leaderboards = leaderboards
    )

@app.route('/teams')
def teams():
    teams = get_teams()

    return render_template(
        'teams.html',
        teams=teams
    )

@app.route('/team/<team_id>')
def team_page(team_id):

    team_data = get_team(team_id)

    return render_template(
        'team.html',
        team=team_data,
        team_id=team_id
    )

@app.route('/team/<team_id>/<int:year_id>/roster')
def teams_roster(team_id, year_id):
    batters, pitchers = get_team_roster(team_id, year_id)

    batting_leaders, pitching_leaders = get_team_stat_leaders(team_id, year_id)

    return render_template(
        'team_roster.html',
        team_id=team_id,
        year_id=year_id,
        batters = batters,
        pitchers = pitchers,
        batting_leaders = batting_leaders,
        pitching_leaders = pitching_leaders
    )
    
@app.route('/awards/<int:year_id>')
def awards(year_id):
    # 1st Iteration 
    # No issues, data is correctly being pulled but the problem is 
    # with the get_awards function with it returning duplicate
    
    awards = get_awards(year_id)
    
    return render_template(
        'awards.html',
        year_id=year_id,
        awards=awards
    )

if __name__ == '__main__':
    app.run(debug=True)