from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq

from src.client import api, logger
from src.services.db.users import get_user_artists

dp = Dispatch()


@dp.callback_query(CallbackDataEq("menu/list_artists"))
async def list_artists(event: CallbackQuery):
    if not event.message:
        return logger.debug(f"{event=}")
    artists = await get_user_artists(event.from_user.id)
    artists_output = [artist.nickname for artist in artists]
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text="\n".join(artists_output),
    )
