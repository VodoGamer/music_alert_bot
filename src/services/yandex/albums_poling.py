import asyncio

from yandex_music import Album, Artist, ArtistAlbums

from src.client import logger
from src.handlers.release_notifications import send_release_notification_to_user
from src.services.db.albums import add_album
from src.services.db.artists import get_all_artists, get_artist_albums_ids, get_artist_fans
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.yandex.artists import get_albums as api_get_albums
from src.services.yandex.artists import get_artist_albums as api_get_artist_albums


async def albums_poling():
    while True:
        await check_albums_on_new()
        await asyncio.sleep(60)


async def check_albums_on_new():
    artists = await get_all_artists()
    if not artists:
        return
    artist_ids = [artist.id for artist in artists]
    logger.debug(f"{artist_ids=}")
    for artist_id in artist_ids:
        artists_albums = await api_get_artist_albums([artist_id])
        missing_album_ids = await find_missing_album_ids(artists_albums, artist_id)
        if not missing_album_ids:
            continue
        for missing_album_id in missing_album_ids:
            if not missing_album_id:
                continue
            missing_album = await api_get_albums([missing_album_id])
            await check_album_on_new(missing_album[0], artist_ids)


async def find_missing_album_ids(
    artists_albums: list[ArtistAlbums | None], artist_id: int
) -> list[int | None] | None:
    if artists_albums[0] is None:
        return logger.error(f"{artists_albums=}")
    artist_album_ids = [album.id for album in artists_albums[0]]
    db_artist_album_ids = await get_artist_albums_ids(int(artist_id)) or artist_album_ids
    missing_album_ids = list(set(artist_album_ids) - set(db_artist_album_ids))
    return missing_album_ids


async def check_album_on_new(album: Album, artist_ids: list[int]):
    if not album.title or not album.id or not album.release_date:
        return logger.error(f"{album=}")
    await add_album(album.id, album.get_cover_url(), album.release_date, album.title)
    for artist in album.artists:
        if artist.id in artist_ids:
            await add_artist_to_collaboration(artist.id, album.id)
        await process_user_notification(artist, album)


async def process_user_notification(artist: Artist, album: Album):
    user_ids = await get_artist_fans(artist.id)
    if user_ids:
        for user_id in user_ids:
            await send_release_notification_to_user(user_id, album, artist)
