select distinct album.* from "user"
join user_favorite_artist ON user_favorite_artist.user_id = "user".id
join collaboration ON collaboration.artist_id = user_favorite_artist.artist_id
join album ON album.id = collaboration.album_id
left join user_listened_album ON user_listened_album.album_id = album.id and user_listened_album.user_id = "user".id
where "user".id = $1 AND user_listened_album is NULL;
