delete from user_listened_album where user_id=$2 and album_id in (select album.id from album join collaboration ON collaboration.album_id = album.id where collaboration.artist_id=$1)
