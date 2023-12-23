import math
from enum import Enum

import msgspec
from telegrinder import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup
from yandex_music import Album

from src.services.db.models import Artist

PAGE_STEP = 5
DELETE_ARTIST_ACTION: str = "delete_artist"


class ArtistSearchAction(Enum):
    correct = "correct_artist_search"
    wrong = "wrong_artist_search"

    def to_dict(self) -> dict:
        return {"action": self.value}


class ArtistSearchData(msgspec.Struct):
    artist_id: int
    action: ArtistSearchAction


def get_correct_or_no_kb(artist_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton(
            "✅ Правильно",
            callback_data=ArtistSearchData(action=ArtistSearchAction.correct, artist_id=artist_id),
        )
    )
    keyboard.add(
        InlineButton(
            "⛔ Неправильно",
            callback_data=ArtistSearchData(action=ArtistSearchAction.wrong, artist_id=artist_id),
        )
    )
    return keyboard.get_markup()


def get_album_link(album: Album) -> str:
    return f"https://music.yandex.ru/album/{album.id}/"


def get_release_link_kb(release: Album) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(InlineButton("Перейти к релизу", url=get_album_link(release)))
    return keyboard.get_markup()


class DeleteArtistData(msgspec.Struct):
    artist_id: int
    action: str = DELETE_ARTIST_ACTION


class PaginationData(msgspec.Struct):
    title: str
    action: str
    page: int | None


def get_remove_artist_kb(artists: list[Artist], page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    pages_count = math.ceil(len(artists) / PAGE_STEP)
    artist_stop_slice = page * PAGE_STEP
    artist_start_slice = (page - 1) * PAGE_STEP

    for artist in artists[artist_start_slice:artist_stop_slice]:
        keyboard.add(InlineButton(artist.nickname, callback_data=DeleteArtistData(artist.id)))
        keyboard.row()
    keyboard.add(
        InlineButton(
            "<-", callback_data=f"delete_artist_nav/previous/{page - 1 if page != 1 else page}"
        )
    )
    keyboard.add(
        InlineButton(f"{page}/{pages_count}", callback_data="delete_artist_nav/list_pages")
    )
    keyboard.add(
        InlineButton(
            "->",
            callback_data=f"delete_artist_nav/next/{page + 1 if page != pages_count else page}",
        )
    )
    return keyboard.get_markup()
