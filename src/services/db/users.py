from src.services.db.artists import register_artist
from src.services.db.models import Album, Artist, User

from . import execute_query, fetch


async def register_user(user_id: int) -> None:
    await execute_query("add_user.sql", user_id)


async def add_artist_to_user_favorites(user_id: int, artist_id: int, artist_nickname: str) -> None:
    await register_user(user_id)
    await register_artist(artist_id, artist_nickname)
    await execute_query("add_artist_to_user.sql", user_id, artist_id)


async def get_user_favorite_artists(user_id: int) -> list[Artist]:
    return await fetch("get_user_favorite_artists.sql", user_id)


async def listen_albums(user_id: int, album_ids: list[int] | list[Album]) -> None:
    for album_id in album_ids:
        await listen_album(user_id, album_id)


async def listen_album(user_id: int, album: int | Album) -> None:
    await execute_query(
        "add_listen_album.sql", user_id, album if isinstance(album, int) else album.id
    )


async def get_all_users() -> list[User]:
    return await fetch("get_all_users.sql")
