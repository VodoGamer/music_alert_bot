from datetime import datetime

from . import MyRecord


class Album(MyRecord):
    id: int
    title: str
    cover_url: str
    release_date: datetime


class Artist(MyRecord):
    id: int
    nickname: str


class Collaboration(MyRecord):
    id: int
    album_id: int
    artist_id: int


class User(MyRecord):
    id: int
