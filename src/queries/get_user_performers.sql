select row_to_json(performer) from user_favorite_performer join performer ON performer.id = user_favorite_performer.performer_id where user_favorite_performer.user_id = $1;
