import asyncio

from src.services.db.artists import get_all_artist_ids
from src.services.yandex.artists import get_artist_albums


async def albums_poling():
    while True:
        artist_ids = [artist["id"] for artist in await get_all_artist_ids()]
        artist_albums = await get_artist_albums(artist_ids)
        await asyncio.sleep(10)
