from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from src.client import api, logger
from src.services.db.users import get_user_favorite_artists

dp = Dispatch()


@dp.message(Text("/list"))
async def list_artists(message: Message):
    artists = await get_user_favorite_artists(message.from_user.id)
    if not artists:
        return logger.error(f"{artists=}")
    await api.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="\n".join([artist[0] for artist in artists]),
    )
