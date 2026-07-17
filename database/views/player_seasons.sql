DROP VIEW IF EXISTS player_seasons;

CREATE VIEW player_seasons AS

SELECT
    player_id,
    Player,
    Team, 
    Year,
    G,
    BA,
    OBP,
    HR,
    RBI,
    WAR
FROM batting_statistics;