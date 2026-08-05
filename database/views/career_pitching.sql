"""
THIS VIEW IS FOR PLAYER PROFILE PAGE
"""
DROP VIEW IF EXISTS career_pitching;

CREATE VIEW career_pitching AS

SELECT

    player_id,
    Player,
    SUM(W) AS Wins,
    SUM(L) AS Losses,
    AVG(ERA) AS CareerERA,
    SUM(SO) AS Strikeouts,
    AVG(WHIP) AS CareerWHIP,
    SUM(WAR) AS CareerWAR

FROM pitching_statistics
GROUP BY 
    player_id,
    Player;