SELECT username, first_name, last_name, 
        handle, goofy, fav_skater, fav_video
FROM auth_user au
JOIN skatebetterapi_skater sk
ON au.id = sk.user_id