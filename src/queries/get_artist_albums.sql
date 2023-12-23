select album.* from album join collaboration ON collaboration.album_id = album.id where collaboration.artist_id = $1;
