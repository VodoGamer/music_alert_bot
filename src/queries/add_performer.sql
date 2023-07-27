insert into performer (id, nickname) values ($1, $2) on conflict do nothing;
