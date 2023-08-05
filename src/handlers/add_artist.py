from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.rules import CallbackDataMarkup, Regex, Text
from telegrinder.types import InputFile
from telegrinder.types import Message as CallbackMessage
from yandex_music import Artist

from src.client import api, gettext, logger
from src.handlers.keyboards import get_correct_or_no_kb
from src.rules.callback_rules import CallbackHasMessageRule
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


@dp.message(
    StateMessageRule(State.WaitArtistNickname),
    Regex(r"https:\/\/music\.yandex\.(?:com|ru)\/artist\/(\d*)\??"),
)
async def artist_link(message: Message, match: tuple[str]):
    artist = await get_artist_by_id(int(match[0]))
    if artist:
        await send_information_about_artist(message, artist)


@dp.message(StateMessageRule(State.WaitArtistNickname))
async def artist_search(message: Message):
    if not message.text:
        return logger.error(f"{message=}")
    artists = await search_artists(message.text)
    if not artists:
        return await api.send_message(chat_id=message.chat.id, text=gettext("artist_not_exist"))
    artist = artists[0]
    await send_information_about_artist(message, artist)


async def send_information_about_artist(message: Message, artist: Artist):
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
            chat_id=message.chat.id,
            caption=gettext("best_result_of_artist_search").format(artist.name),
            photo=InputFile(
                artist.name, await artist.cover.download_bytes_async(size="m1000x1000")
            ),
            reply_markup=get_correct_or_no_kb(artist.id),
        )


@dp.callback_query(CallbackDataMarkup("correct/yes/<artist_id>"), CallbackHasMessageRule())
async def correct_artist(event: CallbackQuery, message: CallbackMessage, artist_id: str):
    await remove_state(event.from_user.id)
    artist = await get_artist_by_id(int(artist_id))
    if not artist or not artist.name:
        return logger.error(f"{artist_id=} {artist=} {event=}")
    await api.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    answer = await api.send_message(chat_id=message.chat.id, text=gettext("albums_initializing"))

    await add_artist_to_user(event.from_user.id, int(artist.id), artist.name)
    await user_albums_init(int(artist_id), event.from_user.id)
    await api.edit_message_text(
        chat_id=message.chat.id,
        message_id=answer.unwrap().message_id,
        text=gettext("user_select_new_artist").format(artist.name),
    )


@dp.callback_query(CallbackDataMarkup("correct/no/<artist_id>"), CallbackHasMessageRule())
async def wrong_artist(event: CallbackQuery, message: CallbackMessage, artist_id: str):
    await remove_state(event.from_user.id)
    await api.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await api.send_message(chat_id=message.chat.id, text=gettext("wrong_artist_search"))
