/*
This page will be used for player batting statistics for each season. 
It will be used to display the player's batting statistics for each season in the app.
*/

DROP VIEW IF EXISTS batting_seasons;

CREATE VIEW batting_seasons AS

SELECT
    player_id,
    Team,
    Year,
    Player,
    Age,
    Pos,
    WAR,
    G,
    PA,
    AB,
    R,
    H,
    "2B",
    "3B",
    HR,
    RBI,
    SB,
    CS,
    BB,
    SO,
    BA,
    OBP,
    SLG,
    OPS,
    "OPS+",
    rOBA,
    "Rbat+",
    TB,
    GIDP,
    HBP,
    SH,
    SF,
    IBB
FROM batting_statistics;