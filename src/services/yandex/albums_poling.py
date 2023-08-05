import asyncio

from yandex_music import Album, Artist

from src.client import logger
from src.handlers.release_notifications import send_release_notification_to_user
from src.services.db.albums import add_album, get_all_albums
from src.services.db.artists import get_all_artists, get_artist_fan_ids
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.db.users import listen_album
from src.services.yandex.artists import get_albums as api_get_albums
from src.services.yandex.artists import get_artist_albums as api_get_artists_albums


async def albums_poling():
    while True:
        await check_albums_on_new()
        await asyncio.sleep(60)


async def check_albums_on_new():
    artist_ids = await _db_get_artist_ids()
    missing_album_ids = await _find_missing_album_ids(artist_ids)
    for missing_album_id in missing_album_ids:
        missing_album = await api_get_albums([missing_album_id])
        await check_album_on_new(missing_album[0], artist_ids)


async def check_album_on_new(album: Album, artist_ids: list[int]):
    if not album.title or not album.id:
        return logger.error(f"{album=}")
    await add_album(album.id, album.get_cover_url(), album.release_date, album.title)
    for artist in album.artists:
        if artist.id in artist_ids:
            await add_artist_to_collaboration(artist.id, album.id)
        await process_user_notification(artist, album)


async def process_user_notification(artist: Artist, album: Album):
    user_ids = await get_artist_fan_ids(artist.id)
    for user_id in user_ids:
        if album.id:
            await listen_album(user_id[0], album.id)
        await send_release_notification_to_user(user_id[0], album, artist)


async def _db_get_artist_ids() -> list[int]:
    artists = await get_all_artists()
    if not artists:
        return []
    artist_ids = [artist.id for artist in artists]
    logger.debug(f"{artist_ids=}")
    return artist_ids


async def _find_missing_album_ids(artist_ids: list[int]) -> list[int]:
    api_albums = await _api_get_album_ids(artist_ids)
    db_model_albums = await get_all_albums()
    db_albums = [db_album.id for db_album in db_model_albums] if db_model_albums else []
    missing_album_ids = list(set(api_albums) - set(db_albums))
    logger.debug(f"{missing_album_ids=}")
    return missing_album_ids


async def _api_get_album_ids(artist_ids: list[int]) -> list[int]:
    api_artists_albums = await api_get_artists_albums(artist_ids)
    api_albums: list[int] = []
    for api_artist_albums in api_artists_albums:
        if not api_artist_albums:
            continue
        for api_album in api_artist_albums.albums:
            if api_album.id:
                api_albums.append(api_album.id)
    return api_albums
