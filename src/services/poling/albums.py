from src.client import bot
from src.services.db.albums import add_album, get_all_albums
from src.services.db.artists import get_all_artists
from src.services.db.collaborations import add_artist_to_collaboration
from src.services.db.models import Artist
from src.services.yandex.artists import get_albums, get_albums_by_artists


@bot.loop_wrapper.interval(seconds=60)
async def albums_poling():
    db_artists = await get_all_artists()
    missing_album_ids = await _find_missing_album_ids(db_artists)
    if not missing_album_ids:
        return
    missing_albums = await get_albums(missing_album_ids)
    for missing_album in missing_albums:
        if not (missing_album.id and missing_album.cover_uri and missing_album.title):
            raise ValueError(missing_album)
        await add_album(
            missing_album.id,
            missing_album.cover_uri,
            missing_album.release_date,
            missing_album.title,
        )
        for artist in missing_album.artists:
            await add_artist_to_collaboration(artist.id, missing_album.id)


async def _find_missing_album_ids(db_artists: list[Artist]) -> list[int] | None:
    api_albums = await get_albums_by_artists([artist.id for artist in db_artists])
    api_album_ids: list[int] = [album.id for album in api_albums if album.id]
    db_albums = await get_all_albums()
    db_album_ids = [album.id for album in db_albums]
    return list(set(api_album_ids) - set(db_album_ids)) or None
