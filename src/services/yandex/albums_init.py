from yandex_music import Album

from src.client import logger
from src.services.db.albums import add_album
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.db.users import listen_album
from src.services.yandex.artists import get_artist_albums as api_get_artists_albums


async def user_albums_init(artist_id: int, user_id: int):
    artists_albums = await api_get_artists_albums([artist_id])
    for artist_albums in artists_albums:
        if not artist_albums:
            continue
        for album in artist_albums.albums:
            await user_album_init(album, artist_id, user_id)


async def user_album_init(album: Album, artist_id: int, user_id: int):
    if not album.title or not album.id:
        return logger.error(f"{album=}")
    await add_album(album.id, album.get_cover_url(), album.release_date, album.title)
    await add_artist_to_collaboration(artist_id, album.id)
    await listen_album(user_id, album.id)
