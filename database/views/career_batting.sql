DROP VIEW IF EXISTS career_batting;

CREATE VIEW career_batting AS

SELECT

    player_id,
    Player,
    SUM(H) AS Hits,
    SUM(HR) AS HomeRuns,
    SUM(RBI) AS RBIs,
    SUM(WAR) AS CareerWAR,
    SUM(H)/SUM(AB) AS CareerAVG

FROM batting_statistics
GROUP BY 
    player_id,
    Player;