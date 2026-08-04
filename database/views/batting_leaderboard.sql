"""
THIS VIEW IS FOR BATTLING LEADERBOARD PAGE
"""

DROP VIEW IF EXISTS batting_leaderboard;

CREATE VIEW batting_leaderboard AS

SELECT
    player_id,
    Player,
    Team,
    Year,
    G,
    BA,
    HR,
    RBI,
    OBP,
    SLG,
    OPS,
    H,
    R,
    BB,
    SB,
    WAR

FROM batting_statistics