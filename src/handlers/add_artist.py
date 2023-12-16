from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.rules import CallbackDataJsonModel, Regex, Text
from telegrinder.types import InputFile
from telegrinder.types import Message as CallbackMessage
from yandex_music import Artist

from src.client import api, gettext
from src.handlers.keyboards import ArtistSearchAction, ArtistSearchData, get_correct_or_no_kb
from src.rules import CallbackDataJsonItemEq, StateMessageRule
from src.services.db.users import add_artist_to_user_favorites
from src.services.states import State, remove_state, set_state
from src.services.yandex.albums_init import artist_albums_init
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
    if not artist:
        raise ValueError
    await send_information_about_artist(message, artist)


@dp.message(StateMessageRule(State.WaitArtistNickname))
async def artist_search(message: Message):
    artists = await search_artists(message.text.unwrap())
    if not artists:
        return await api.send_message(chat_id=message.chat.id, text=gettext("artist_not_exist"))
    artist = artists[0]
    await send_information_about_artist(message, artist)


async def send_information_about_artist(message: Message, artist: Artist):
    if not artist.name:
        await message.answer(text=gettext("artist_not_exist"))
    elif not artist.cover:
        await message.answer(
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


@dp.callback_query(
    CallbackDataJsonItemEq(ArtistSearchAction.correct.to_dict()),
    CallbackDataJsonModel(ArtistSearchData),
)
async def correct_artist_search(event: CallbackQuery, data: ArtistSearchData):
    message: CallbackMessage = event.message.unwrap()
    await remove_state(event.from_user.id)
    artist = await get_artist_by_id(data.artist_id)
    if not artist or not artist.name:
        raise ValueError(f"{artist=}")
    await api.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    answer = (
        await api.send_message(chat_id=message.chat.id, text=gettext("albums_initializing"))
    ).unwrap()
    await add_artist_to_user_favorites(event.from_user.id, int(artist.id), artist.name)
    await artist_albums_init(data.artist_id, event.from_user.id)
    await api.edit_message_text(
        chat_id=message.chat.id,
        message_id=answer.message_id,
        text=gettext("user_select_new_artist").format(artist.name),
    )


@dp.callback_query(
    CallbackDataJsonItemEq(ArtistSearchAction.wrong.to_dict()),
    CallbackDataJsonModel(ArtistSearchData),
)
async def wrong_artist_search(event: CallbackQuery):
    message: CallbackMessage = event.message.unwrap()
    await remove_state(event.from_user.id)
    await api.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await api.send_message(chat_id=message.chat.id, text=gettext("wrong_artist_search"))
