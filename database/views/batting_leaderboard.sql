/*
THESE VIEWS ARE WORKING AS DATA PROVIDERS FOR DIFFERENT PAGES IN THE APP

THIS VIEW IS FOR BATTLING LEADERBOARD PAGE
*/

DROP VIEW IF EXISTS batting_leaderboard;

CREATE VIEW batting_leaderboard AS

SELECT
    player_id,
    Team,
    Year,
    Player,
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
    TB,
    GIDP,
    HBP,
    IBB

FROM batting_statistics;