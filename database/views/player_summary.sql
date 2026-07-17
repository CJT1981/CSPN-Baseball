DROP VIEW IF EXISTS player_summary;

CREATE VIEW player_summary AS 

SELECT

    p.player_id,
    p.player_name,
    p.position,
    p.height,
    p.weight,
    p.birth_date,
    p.bats,
    p.throws,

FROM player_profiles p;