import math

from telegrinder import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup
from yandex_music import Album

from src.services.db.models import Artist

PAGE_STEP = 5


def get_correct_or_no_kb(artist_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(InlineButton("✅ Правильно", callback_data=f"correct/yes/{artist_id}"))
    keyboard.add(InlineButton("⛔ Неправильно", callback_data=f"correct/no/{artist_id}"))
    return keyboard.get_markup()


def get_release_link_kb(release: Album) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Перейти к релизу", url=f"https://music.yandex.ru/album/{release.id}/")
    )
    return keyboard.get_markup()


def get_remove_artist_kb(artists: list[Artist], page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    pages_count = math.ceil(len(artists) / PAGE_STEP)
    artist_stop_slice = page * PAGE_STEP
    artist_start_slice = (page - 1) * PAGE_STEP

    for artist in artists[artist_start_slice:artist_stop_slice]:
        keyboard.add(InlineButton(artist.nickname, callback_data=f"delete_artist/{artist.id}"))
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
