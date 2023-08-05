from src.services.db import execute_query, fetch
from src.services.db.artists import register_artist
from src.services.db.models import Artist


async def register_user(user_id: int) -> None:
    await execute_query("add_user.sql", user_id)


async def add_artist_to_user(user_id: int, artist_id: int, artist_nickname: str) -> None:
    await register_user(user_id)
    await register_artist(artist_id, artist_nickname)
    await execute_query("add_artist_to_user.sql", user_id, artist_id)


async def get_user_favorite_artists(user_id: int) -> list[Artist]:
    return await fetch("get_user_favorite_artists.sql", user_id)


async def listen_album(user_id: int, album_id: int) -> None:
    await execute_query("add_listen_album.sql", user_id, album_id)
