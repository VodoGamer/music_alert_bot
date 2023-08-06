from datetime import datetime

from src.services.db import execute_query, fetch
from src.services.db.models import Album


async def add_album(id: int, cover_url: str, release_date_str: str | None, title: str) -> None:
    release_date = datetime.now(tz=None)
    if release_date_str:
        release_date = datetime.fromisoformat(release_date_str).replace(tzinfo=None)
    await execute_query("add_album.sql", id, cover_url, release_date, title)


async def get_all_albums() -> list[Album]:
    return await fetch("get_all_albums.sql")
