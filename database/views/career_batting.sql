/*
THIS VIEW IS FOR PLAYER PROFILE PAGE
*/
DROP VIEW IF EXISTS career_batting;

CREATE VIEW career_batting AS

SELECT

    player_id,
    Player,
    SUM(G) AS cG,
    SUM(H) AS cHits,
    SUM(HR) AS cHomeRuns,
    SUM('2B') AS cDoubles,
    SUM('3B') AS cTriples,
    SUM(RBI) AS cRBIs,
    SUM(WAR) AS cWAR,
    AVG(BA) AS cAVG,
    AVG(OBP) AS cOBP,
    AVG(SLG) AS cSLG,
    AVG(OPS) AS cOPS

FROM batting_statistics
GROUP BY 
    player_id,
    Player;