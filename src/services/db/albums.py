from datetime import datetime

from src.services.db.main import execute_query, fetch


async def get_artist_albums(artist_id: int):
    await fetch("get_artist_albums.sql", artist_id)


async def add_album(id: int, cover_url: str, release_str: str, title: str):
    release_date = datetime.fromisoformat(release_str).replace(tzinfo=None)
    await execute_query("add_album.sql", id, cover_url, release_date, title)
