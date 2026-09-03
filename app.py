from flask import Flask, render_template
from database.queries import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Creating a route for the player profile page
@app.route('/player/<player_id>')
def player_profile(player_id):
    # TEST #3:

    # GET PLAYER PROFILE
    profile_data = get_player_profile(player_id)

    # If there is no profile data, return a 404 error page
    if profile_data.empty:
        return "Player not found", 404

    # DETERMINE IF PLAYER IS A PITCHER OR NON-PITCHER
    profile = profile_data.iloc[0].to_dict()
    
    # Because we pulled a whole Panda series, we need to pull the position from the 
    # series to determine if we need to pull pitching or batting stats.
    # Here is where we pull the position:
    position = profile['position']

    player_season_stats = None

    # Here is where we determine if the player is a pitcher or not, 
    # and then pull the appropriate stats.
    if 'Pitcher' in position or 'P' in position:
        player_career_stats = get_player_career_pitching(player_id)
        player_season_stats = get_pitching_seasons(player_id)
    else:
        player_career_stats = get_player_career_batting(player_id)
        player_season_stats = get_batting_seasons(player_id)
        """
        print("========== CAREER STATS ==========")
        print(player_career_stats)
        print("Is empty:", player_career_stats.empty)
        print("Columns:", player_career_stats.columns.tolist())
        print("==================================")"""

    # SEND OUR DATA TO HTML
    return render_template(
        "player_profile.html",
        profile=profile,
        player_career_stats=player_career_stats,
        player_season_stats=player_season_stats

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

if __name__ == '__main__':
    app.run(debug=True)