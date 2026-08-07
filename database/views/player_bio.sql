/*
THIS VIEW IS FOR PLAYER PROFILE PAGE
*/

DROP VIEW IF EXISTS player_bio;

CREATE VIEW player_bio AS 

SELECT

    p.player_id,
    p.player_name,
    p.position,
    p.height,
    p.weight,
    p.birth_date,
    p.bats,
    p.throws

FROM player_profiles p;