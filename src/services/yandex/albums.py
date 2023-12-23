from yandex_music import Album

from .api import get_yandex_api


async def get_albums(album_ids: list[int]) -> list[Album]:
    api = await get_yandex_api()
    return await api.albums(list(map(int, album_ids)))
