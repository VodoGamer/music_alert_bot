from datetime import datetime

import ujson
from pydantic import BaseModel

from src.services.db.main import execute_query, fetch


class Album(BaseModel):
    id: int
    title: str
    cover_url: str
    release_date: datetime


async def get_artist_albums(artist_id: int):
    await fetch("get_artist_albums.sql", artist_id)


async def add_album(id: int, cover_url: str, release_str: str, title: str):
    release_date = datetime.fromisoformat(release_str).replace(tzinfo=None)
    await execute_query("add_album.sql", id, cover_url, release_date, title)


async def get_album(album_id: int) -> Album | None:
    album = await fetch("get_album.sql", album_id)
    if album == []:
        return None
    return Album(**ujson.loads(album[0][0]))
