from src.services.db.main import execute_query


async def add_artist_to_collaboration(artist_id: int, album_id: int):
    await execute_query("add_artist_to_collaboration.sql", artist_id, album_id)
