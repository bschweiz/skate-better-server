SELECT username, first_name, last_name, 
        handle, goofy, fav_skater, fav_video
FROM auth_user au
JOIN skatebetterapi_skater sk
ON au.id = sk.user_id

DELETE FROM skatebetterapi_opponent AS o
WHERE o.id  > 3

DELETE FROM skatebetterapi_gametrick AS gt
WHERE gt.id  > 18

DELETE FROM skatebetterapi_game AS g
WHERE g.id  > 3

SELECT *
FROM authtoken_token

SELECT *
FROM skatebetterapi_gametrick

SELECT *
FROM skatebetterapi_game

SELECT *
FROM skatebetterapi_opponent


-- AVAILABLE Tricks using GameTrick.game_id as filter
SELECT t.id, t.name
FROM skatebetterapi_trick AS t
WHERE t.id NOT IN 

        (SELECT t.id
        FROM skatebetterapi_gametrick AS gt
        JOIN skatebetterapi_game AS g
        ON gt.game_id = g.id
        JOIN skatebetterapi_trick AS t
        ON gt.trick_id = t.id
        WHERE gt.game_id = 1) 