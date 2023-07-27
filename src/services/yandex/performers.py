from dataclasses import dataclass

import aiohttp
from yandex_music import Artist

from src.client import yandex_client


@dataclass(frozen=True, slots=True)
class PerformerSearch:
    nickname: str
    cover: bytes | None


async def get_performer_info(performer_nickname) -> Artist | None:
    return await _search_performers(performer_nickname)


async def get_performer_cover(nickname: str) -> PerformerSearch | None:
    return await _get_performer_info_from_search(await _search_performers(nickname))


async def _search_performers(nickname: str) -> Artist | None:
    api = await yandex_client.init()
    search_result = await api.search(nickname, type_="artist")
    if search_result and search_result.artists:
        return search_result.artists.results[0]


async def _get_performer_info_from_search(artist: Artist | None) -> PerformerSearch | None:
    if artist and artist.name and artist.cover:
        return PerformerSearch(artist.name, await _download_performer_cover(artist.cover.uri))


async def _download_performer_cover(url: str | None) -> bytes | None:
    if url is None:
        return
    fine_url = url.split("/")[:-1]
    fine_url.append("200x200")  # TODO: change to method variable
    fine_url = "/".join(fine_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://{fine_url}") as resp:
            return await resp.read()
