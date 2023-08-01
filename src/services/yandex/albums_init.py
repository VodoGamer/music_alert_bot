from yandex_music import Album

from src.client import logger
from src.services.db.albums import add_album
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.yandex.artists import get_artist_albums as api_get_artist_albums


async def albums_init(artist_id: int):
    artists_albums = await api_get_artist_albums([artist_id])
    if not artists_albums:
        return logger.error(f"{artists_albums=}")
    for artist_albums in artists_albums:
        if not artist_albums:
            continue
        for album in artist_albums.albums:
            await album_init(album, artist_id)


async def album_init(album: Album, artist_id: int):
    if not album.release_date or not album.title or not album.id:
        return logger.error(f"{album=}")
    await add_album(album.id, album.getCoverUrl(), album.release_date, album.title)
    await add_artist_to_collaboration(artist_id, album.id)
