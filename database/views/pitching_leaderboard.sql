"""
THIS VIEW IS FOR PITCHING LEADERBOARD PAGE
"""

DROP VIEW IF EXISTS pitching_leaderboard;

CREATE VIEW pitching_leaderboard AS

SELECT
    player_id,
    Player,
    Team,
    Year,
    G,
    W,
    L,
    ERA,
    SO,
    BB,
    WHIP,
    WAR
FROM pitching_statistics