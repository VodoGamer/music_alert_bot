from datetime import datetime
from typing import NamedTuple


class Album(NamedTuple):
    id: int
    title: str
    cover_url: str
    release_date: datetime


class Artist(NamedTuple):
    id: int
    nickname: str


class Collaboration(NamedTuple):
    id: int
    album_id: int
    artist_id: int


class User(NamedTuple):
    id: int
