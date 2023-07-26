"""simple dispatch"""
from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text

from src.client import api

dp = Dispatch()


@dp.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello, {message.from_user.username}, I am {me.first_name} bot!")
