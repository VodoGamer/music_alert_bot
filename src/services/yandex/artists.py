from yandex_music import Album, Artist, ArtistAlbums

from .api import get_yandex_api


async def get_albums_by_artist_ids(artist_ids: list[int]) -> list[Album]:
    api_artists_albums = await _get_artists_albums(artist_ids)
    api_albums: list[Album] = []
    for api_artist_albums in api_artists_albums:
        if not api_artist_albums:
            continue
        for api_album in api_artist_albums.albums:
            if api_album:
                api_albums.append(api_album)
    return api_albums


async def _get_artists_albums(artist_ids: list[int]) -> list[ArtistAlbums | None]:
    api = await get_yandex_api()
    artists_albums: list[ArtistAlbums | None] = []
    for artist_id in artist_ids:
        artists_albums.append(await api.artists_direct_albums(artist_id, page_size=0))
    return artists_albums


async def search_artists(nickname: str) -> list[Artist] | None:
    api = await get_yandex_api()
    search_result = await api.search(nickname, type_="artist")
    if search_result and search_result.artists:
        return search_result.artists.results


async def get_artist_by_id(id: int) -> Artist | None:
    api = await get_yandex_api()
    artists = await api.artists([id])
    return artists[0]
