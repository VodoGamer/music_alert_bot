from . import execute_query


async def add_artist_to_collaboration(artist_id: int, album_id: int) -> None:
    await execute_query("add_artist_to_collaboration.sql", *locals().values())
