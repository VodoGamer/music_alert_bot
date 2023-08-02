import asyncio

from yandex_music import Album, Artist

from src.client import logger
from src.handlers.release_notifications import send_release_notification_to_user
from src.services.db.albums import add_album, get_album
from src.services.db.artists import get_all_artist_ids
from src.services.db.users import get_artist_fans
from src.services.yandex.artists import get_artist_albums as api_get_artist_albums


async def albums_poling():
    while True:
        artist_ids = [artist["id"] for artist in await get_all_artist_ids()]
        artists_albums = await api_get_artist_albums(artist_ids)
        if not artists_albums:
            return logger.error(f"{artists_albums=}")
        for artist_albums in artists_albums:
            if not artist_albums:
                return logger.error(f"{artist_albums=}")
            for album in artist_albums:
                await check_album_on_new(album)
        await asyncio.sleep(60)


async def check_album_on_new(album: Album):
    if not album.title or not album.id or not album.release_date:
        return logger.error(f"{album=}")
    if await get_album(album.id):
        return None
    await add_album(album.id, album.get_cover_url(), album.release_date, album.title)
    for artist in album.artists:
        await process_user_notification(artist, album)


async def process_user_notification(artist: Artist, album: Album):
    user_ids = await get_artist_fans(artist.id)
    if user_ids:
        for user_id in user_ids:
            await send_release_notification_to_user(user_id, album)
