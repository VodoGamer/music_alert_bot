insert into album (id, cover_url, release_date, title) values ($1, $2, $3, $4) on conflict do nothing;
