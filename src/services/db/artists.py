from pydantic import BaseModel

from src.services.db.main import execute_query


class Artist(BaseModel):
    id: int
    nickname: str


async def register_artist(artist_id: int, artist_nickname: str):
    await execute_query("add_artist.sql", artist_id, artist_nickname)
