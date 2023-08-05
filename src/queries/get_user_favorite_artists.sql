select artist.id, artist.nickname from user_favorite_artist join artist ON artist.id = user_favorite_artist.artist_id where user_favorite_artist.user_id = $1 order by artist.nickname;
