SELECT username, first_name, last_name, 
        handle, goofy, fav_skater, fav_video
FROM auth_user au
JOIN skatebetterapi_skater sk
ON au.id = sk.user_id

DELETE FROM skatebetterapi_opponent AS o
WHERE o.id  > 3

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
