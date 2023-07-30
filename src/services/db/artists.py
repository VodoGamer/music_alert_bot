from typing import TypedDict

from pydantic import BaseModel

from src.services.db.main import execute_query, fetch


class Artist(BaseModel):
    id: int
    nickname: str


class ArtistIdsReturn(TypedDict):
    id: int | str


async def register_artist(artist_id: int, artist_nickname: str):
    await execute_query("add_artist.sql", artist_id, artist_nickname)


async def get_all_artist_ids() -> list[ArtistIdsReturn]:
    return await fetch("get_artist_ids.sql")
