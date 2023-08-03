from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq

from src.client import api, logger
from src.services.db.users import get_user_favorite_artists

dp = Dispatch()


@dp.callback_query(CallbackDataEq("menu/list_artists"))
async def list_artists(event: CallbackQuery):
    artists = await get_user_favorite_artists(event.from_user.id)
    if not event.message or not artists:
        return logger.error(f"{event=} {artists=}")
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text="\n".join([artist.nickname for artist in artists]),
    )
