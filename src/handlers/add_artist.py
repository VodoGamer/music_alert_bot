import re

from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.rules import CallbackDataMarkup, Text
from telegrinder.types import InputFile

from src.client import api, gettext, logger
from src.handlers.keyboards import get_correct_or_no_kb
from src.rules.state_rules import StateMessageRule
from src.services.db.users import add_artist_to_user
from src.services.states import State, remove_state, set_state
from src.services.yandex.albums_init import user_albums_init
from src.services.yandex.artists import get_artist_by_id, search_artists

dp = Dispatch()


@dp.message(Text("/add_artist"))
async def add_artist(message: Message):
    await message.answer(text=gettext("request_artist_nickname"))
    await set_state(message.from_user.id, State.WaitArtistNickname)


@dp.message(StateMessageRule(State.WaitArtistNickname))
async def artist_search(message: Message):
    if not message.text:
        return logger.error(f"{message=}")
    if not message.text.startswith("https://"):
        artists = await search_artists(message.text)
        if not artists:
            return await api.send_message(
                chat_id=message.chat.id, text=gettext("artist_not_exist")
            )
        artist = artists[0]
    else:
        match = re.match(r"https:\/\/music\.yandex\.com\/artist\/(\d*)\??", message.text)
        if not match:
            return
        artist = await get_artist_by_id(int(match.groups()[0]))
        if not artist:
            return
    if not artist.name:
        await api.send_message(chat_id=message.chat.id, text=gettext("artist_not_exist"))
    elif not artist.cover:
        await api.send_message(
            chat_id=message.chat.id,
            text=gettext("best_result_of_artist_search").format(artist.name),
            reply_markup=get_correct_or_no_kb(artist.id),
        )
    else:
        await api.send_photo(
            message.chat.id,
            caption=gettext("best_result_of_artist_search").format(artist.name),
            photo=InputFile(
                artist.name, await artist.cover.download_bytes_async(size="m1000x1000")
            ),
            reply_markup=get_correct_or_no_kb(artist.id),
        )


@dp.callback_query(CallbackDataMarkup("correct/yes/<artist_id>"))
async def correct_artist(event: CallbackQuery, artist_id: str):
    artist = await get_artist_by_id(int(artist_id))
    if not artist or not artist.name or not event.message:
        return logger.error(f"{artist_id=} {artist=} {event=}")
    await add_artist_to_user(event.from_user.id, int(artist.id), artist.name)

    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await user_albums_init(int(artist_id), event.from_user.id)
    await api.send_message(
        chat_id=event.message.chat.id,
        text=gettext("user_select_new_artist").format(artist.name),
    )
    await remove_state(event.from_user.id)


@dp.callback_query(CallbackDataMarkup("correct/no/<artist_id>"))
async def wrong_artist(event: CallbackQuery, artist_id: str):
    if not event.message:
        return logger.debug(f"{event=}")
    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await api.send_message(
        chat_id=event.message.chat.id,
        text=gettext("wrong_artist_search"),
    )
    await remove_state(event.message.from_user.id)
