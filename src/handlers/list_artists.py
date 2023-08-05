from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from src.services.db.users import get_user_favorite_artists

dp = Dispatch()


@dp.message(Text("/list"))
async def list_artists(message: Message):
    artists = await get_user_favorite_artists(message.from_user.id)
    await message.answer("\n".join([artist.nickname for artist in artists]))
