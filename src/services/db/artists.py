from src.services.db import execute_query, fetch
from src.services.db.models import Artist


async def register_artist(artist_id: int, artist_nickname: str) -> None:
    await execute_query("add_artist.sql", *locals().values())


async def get_all_artists() -> list[Artist] | None:
    return await fetch("get_all_artists.sql")


async def get_artist_albums_ids(artist_id: int) -> list[int] | None:
    album_ids = await fetch("get_artist_albums_ids.sql", *locals().values())
    if album_ids:
        return [album_id[0] for album_id in album_ids]


async def get_artist_fans(artist_id: int) -> list[int] | None:
    return await fetch("get_artist_fans.sql", artist_id)
