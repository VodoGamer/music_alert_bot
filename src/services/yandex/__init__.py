import aiohttp


async def download_cover(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            return await resp.read()
