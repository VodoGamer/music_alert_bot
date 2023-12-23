from yandex_music import Album

from src.services.db.albums import add_album
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.db.users import listen_album
from src.services.yandex.artists import get_albums_by_artist_ids


async def init_artist_albums(artist_id: int, user_id: int):
    albums = await get_albums_by_artist_ids([artist_id])
    for album in albums:
        await _init_album_for_user(album, artist_id, user_id)


async def _init_album_for_user(album: Album, artist_id: int, user_id: int):
    if not album.title or not album.id:
        raise ValueError(album)
    await add_album(album.id, album.get_cover_url(), album.release_date, album.title)
    await add_artist_to_collaboration(artist_id, album.id)
    await listen_album(user_id, album.id)
