DROP VIEW IF EXISTS team_roster;

CREATE VIEW team_roster AS

SELECT
    player_id,
    Player,
    Team, 
    Year,
    Pos,
    G,
    BA,
    OBP,
    HR,
    RBI,
    WAR