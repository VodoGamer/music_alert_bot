import ujson

from src.services.db.artists import Artist, register_artist
from src.services.db.main import execute_query, fetch


async def register_user(user_id: int):
    await execute_query("add_user.sql", user_id)


async def add_artist_to_user(user_id: int, artist_id: int, artist_nickname: str):
    await register_user(user_id)
    await register_artist(artist_id, artist_nickname)
    await execute_query("add_artist_to_user.sql", user_id, artist_id)


async def get_user_artists(user_id: int) -> list[Artist]:
    artists = await fetch("get_user_artists.sql", user_id)
    return [Artist(**ujson.loads(artist[0])) for artist in artists]
