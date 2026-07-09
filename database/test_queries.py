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