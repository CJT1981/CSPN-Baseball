"""
from queries import top_batting_average, top_home_runs, team_HR_leaders, best_OPS_per_season, best_OPS_seasons

query1_results = top_batting_average(2012)

print(query1_results)

query2_results = top_home_runs(2004)

print(query2_results)

query3_results = team_HR_leaders(2004)

print(query3_results)

query4_results = best_OPS_per_season(2000, 2025)

print(query4_results)

query5_results = best_OPS_seasons(2000, 2025)

print(query5_results)
"""

from queries import *

print("=" * 25)
print("TESTING PLAYER PROFILE")
print("=" * 25)

# Testing to get player profile for Barry Bonds
player = get_player_profile("bondsba01")
print(player)

print("\n")

print("=" * 25)
print("TESTING CAREER BATTING")
print("=" * 25)

career_batting = get_player_career_batting("troutmi01")
print(career_batting)

print("\n")

print("=" * 25)
print("TESTING CAREER PITCHING")
print("=" * 25)

career_pitching = get_player_career_pitching("maddugr01")
print(career_pitching)

print("\n")

print("=" * 25)
print("TESTING BATTING SEASONS")
print("=" * 25)

batting_seasons = get_batting_seasons("cabreas01")
print(batting_seasons)

print("\n")

print("=" * 25)
print("TESTING PITCHING SEASONS")
print("=" * 25)

pitching_seasons = get_pitching_seasons("scherma01")
print(pitching_seasons)

print("\n")

print("=" * 25)
print("TESTING TEAM")
print("=" * 25)

team = get_team("BOS", 2011)
print(team)

print("\n")

print("=" * 25)
print("TESTING TEAM ROSTER")
print("=" * 25)

batting_roster, pitching_roster = get_team_roster("LAD", 2023)
print("POSITION PLAYERS")
print(batting_roster)
print("PITCHING PLAYERS")
print(pitching_roster)

print("\n")

"""
print("=" * 25)
print("TESTING PLAYER SEARCH")
print("=" * 25)

players = get_player_search("%trout%")
print(players)
"""
print("\n")

print("=" * 25)
print("TESTING BATTING LEADERS")
print("=" * 25)

leaders = get_batting_leaders("HR", 2023)
print(leaders)

print("\n")

print("=" * 25)
print("TESTING PITCHING LEADERS")
print("=" * 25)

leaders = get_pitching_leaders("SO", 2023)
print(leaders)