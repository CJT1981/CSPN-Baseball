/*
THIS VIEW IS FOR PITCHING LEADERBOARD PAGE
*/

DROP VIEW IF EXISTS pitching_leaderboard;

CREATE VIEW pitching_leaderboard AS

SELECT
    player_id,
    Team,
    Year,
    Player,
    WAR,
    W,
    L,
    "W-L%",
    ERA,
    G,
    GS,
    GF,
    CG,
    SHO,
    SV,
    IP,
    H,
    R,
    ER,
    HR,
    BB,
    SO,
    HBP,
    "ERA+",
    FIP,
    WHIP,
    H9,
    HR9,
    BB9,
    SO9,
    "SO/BB"
FROM pitching_statistics;