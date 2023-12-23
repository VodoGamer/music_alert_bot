from src.services.db import execute_query, fetch
from src.services.db.models import Artist


async def register_artist(artist_id: int, artist_nickname: str) -> None:
    await execute_query("add_artist.sql", *locals().values())


async def get_all_artists() -> list[Artist]:
    return await fetch("get_all_artists.sql")


async def delete_artist_from_favorite(artist_id: int, user_id: int) -> None:
    await execute_query("delete_artist_from_favorite.sql", *locals().values())
    await execute_query("delete_user_listened_album.sql", *locals().values())
