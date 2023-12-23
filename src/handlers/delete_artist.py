from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.rules import CallbackDataJsonModel, CallbackDataMarkup, Text

from src.client import api, gettext
from src.handlers.keyboards import DELETE_ARTIST_ACTION, DeleteArtistData, get_remove_artist_kb
from src.rules import CallbackDataJsonItemEq
from src.services.db.artists import delete_artist_from_favorite
from src.services.db.users import get_user_favorite_artists
from src.services.yandex import get_artist_by_id

dp = Dispatch()


@dp.message(Text("/delete_artist"))
async def delete_artist(message: Message):
    artists = await get_user_favorite_artists(message.from_user.id)
    await message.answer(
        gettext("choose_artist_for_delete"), reply_markup=get_remove_artist_kb(artists, 1)
    )


@dp.callback_query(CallbackDataMarkup("delete_artist_nav/<direction>/<page>"))
async def delete_artist_nav(event: CallbackQuery, page: str):
    message = event.message.unwrap()
    artists = await get_user_favorite_artists(event.from_user.id)
    await api.edit_message_reply_markup(
        message.chat.id,
        message.message_id,
        reply_markup=get_remove_artist_kb(artists, int(page)),
    )


@dp.callback_query(
    CallbackDataJsonModel(DeleteArtistData), CallbackDataJsonItemEq("action", DELETE_ARTIST_ACTION)
)
async def delete_artist_button(event: CallbackQuery, data: DeleteArtistData):
    message = event.message.unwrap()
    artist = await get_artist_by_id(int(data.artist_id))
    if not artist:
        raise ValueError
    await delete_artist_from_favorite(int(data.artist_id), event.from_user.id)
    await api.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await api.send_message(
        chat_id=message.chat.id, text=gettext("artist_has_been_deleted").format(artist.name)
    )
