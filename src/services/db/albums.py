from datetime import datetime

from src.services.db import execute_query


async def add_album(id: int, cover_url: str, release_str: str, title: str) -> None:
    release_date = datetime.fromisoformat(release_str).replace(tzinfo=None)
    await execute_query("add_album.sql", id, cover_url, release_date, title)
