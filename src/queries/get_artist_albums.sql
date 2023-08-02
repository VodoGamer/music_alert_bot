select row_to_json(album) from album where artist_id=$1;
