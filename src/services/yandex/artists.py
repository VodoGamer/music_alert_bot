import aiohttp
from yandex_music import Artist, ClientAsync, Cover

from src.client import yandex_client


async def search_artists(nickname: str) -> list[Artist] | None:
    api = await _get_yandex_api()
    search_result = await api.search(nickname, type_="artist")
    if search_result and search_result.artists:
        return search_result.artists.results


async def download_artist_cover(url: Cover) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url.get_url()) as resp:
            return await resp.read()


async def get_artist_by_id(id: int) -> Artist | None:
    api = await _get_yandex_api()
    artists = await api.artists([id])
    return artists[0]


async def _get_yandex_api() -> ClientAsync:
    if not getattr(_get_yandex_api, "api", None):
        api = await yandex_client.init()
        _get_yandex_api.api = api
    return _get_yandex_api.api
