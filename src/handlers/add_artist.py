from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq, CallbackDataMarkup
from telegrinder.types import InputFile

from src.client import api, dispatch, gettext, logger
from src.handlers.keyboards import get_correct_or_no_kb
from src.services.db.users import add_artist_to_user
from src.services.yandex.albums_init import albums_init
from src.services.yandex.artists import (
    download_artist_cover,
    get_artist_by_id,
    search_artists,
)

dp = Dispatch()


@dp.callback_query(CallbackDataEq("menu/add_artist"))
async def add_artist(event: CallbackQuery):
    if not event.message:
        return logger.error(f"{event=}")
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text=gettext("request_artist_nickname"),
    )
    answer, _ = await dispatch.message.wait_for_message(event.message.chat.id)
    if not answer.text:
        return logger.error(f"{answer=}")
    artists = await search_artists(answer.text)
    if not artists:
        return await api.send_message(chat_id=answer.chat.id, text=gettext("artist_not_exist"))
    artist = artists[0]
    if not artist.name:
        await api.send_message(chat_id=answer.chat.id, text=gettext("artist_not_exist"))
    elif not artist.cover:
        await api.send_message(
            chat_id=answer.chat.id,
            text=gettext("best_result_of_artist_search").format(artist.name),
            reply_markup=get_correct_or_no_kb(artist.id),
        )
    else:
        await api.send_photo(
            answer.chat.id,
            caption=gettext("best_result_of_artist_search").format(artist.name),
            photo=InputFile(artist.name, await download_artist_cover(artist.cover)),
            reply_markup=get_correct_or_no_kb(artist.id),
        )


@dp.callback_query(CallbackDataMarkup("correct/yes/<artist_id>"))
async def correct_artist(event: CallbackQuery, artist_id: str):
    artist = await get_artist_by_id(int(artist_id))
    if not artist or not artist.name or not event.message:
        return logger.error(f"{artist_id=} {artist=} {event=}")
    await add_artist_to_user(event.from_user.id, int(artist.id), artist.name)

    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await albums_init(int(artist_id))
    await api.send_message(
        chat_id=event.message.chat.id,
        text=gettext("user_select_new_artist").format(artist.name),
    )


@dp.callback_query(CallbackDataEq("correct/no"))
async def wrong_artist(event: CallbackQuery):
    if not event.message:
        return logger.debug(f"{event=}")
    await api.edit_message_text(chat_id=event.message.chat.id, text=gettext("wrong_artist_search"))
