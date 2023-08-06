import asyncio
from datetime import datetime, timedelta, timezone

from yandex_music import Album, Artist

from src.client import logger
from src.handlers.release_notifications import send_release_notification_to_user
from src.services.db.albums import add_album, get_all_albums
from src.services.db.artists import get_all_artists, get_artist_fan_ids
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.db.users import listen_album
from src.services.yandex.artists import get_albums as api_get_albums
from src.services.yandex.artists import get_artist_albums as api_get_artists_albums


async def albums_poling_by_time():
    while True:
        tz = timezone(timedelta(hours=3))  # UTC+3 for Moscow Time
        now = datetime.now(tz=tz)
        midnight = now.replace(hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
        wait_seconds = (midnight - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await sync_all_albums()


async def albums_auto_poling():
    while True:
        await sync_all_albums()
        await asyncio.sleep(60)


async def sync_all_albums():
    artist_ids = await _db_get_artist_ids()
    missing_album_ids = await _find_missing_album_ids(artist_ids)
    for missing_album_id in missing_album_ids:
        missing_album = await api_get_albums([missing_album_id])
        await sync_album(missing_album[0], artist_ids)


async def sync_album(album: Album, artist_ids: list[int]):
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
    artist_ids = [artist.id for artist in await get_all_artists()]
    logger.debug(f"{artist_ids=}")
    return artist_ids


async def _find_missing_album_ids(artist_ids: list[int]) -> list[int]:
    api_album_ids = await _api_get_album_ids(artist_ids)
    db_album_ids = [db_album.id for db_album in await get_all_albums()]
    missing_album_ids = list(set(api_album_ids) - set(db_album_ids))
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
