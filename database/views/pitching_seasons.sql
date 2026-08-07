/*
This page will be used for player pitching statistics for each season. 
It will be used to display the player's pitching statistics for each season in the app.
*/

DROP VIEW IF EXISTS pitching_seasons;

CREATE VIEW pitching_seasons AS

SELECT
    player_id,
    Team,
    Year,
    Player,
    Age,
    Pos,
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
    IBB,
    SO,
    HBP,
    BK,
    WP,
    BF,
    "ERA+",
    FIP,
    WHIP,
    H9,
    HR9,
    BB9,
    SO9,
    "SO/BB"

FROM pitching_statistics;