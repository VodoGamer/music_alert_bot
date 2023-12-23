from yandex_music import Album, Artist, ArtistAlbums

from src.client import yandex_client


async def get_artists_albums(artist_ids: list[int]) -> list[ArtistAlbums | None]:
    api = await yandex_client.init()
    artists_albums: list[ArtistAlbums | None] = []
    for artist_id in artist_ids:
        artists_albums.append(await api.artists_direct_albums(artist_id, page_size=0))
    return artists_albums


async def get_albums_by_artists(artist_ids: list[int]) -> list[Album]:
    api_artists_albums = await get_artists_albums(artist_ids)
    api_albums: list[Album] = []
    for api_artist_albums in api_artists_albums:
        if not api_artist_albums:
            continue
        for api_album in api_artist_albums.albums:
            if api_album:
                api_albums.append(api_album)
    return api_albums


async def get_albums(album_ids: list[int]) -> list[Album]:
    api = await yandex_client.init()
    return await api.albums(list(map(int, album_ids)))


async def search_artists(nickname: str) -> list[Artist] | None:
    api = await yandex_client.init()
    search_result = await api.search(nickname, type_="artist")
    if search_result and search_result.artists:
        return search_result.artists.results


async def get_artist_by_id(id: int) -> Artist | None:
    api = await yandex_client.init()
    artists = await api.artists([id])
    return artists[0]
