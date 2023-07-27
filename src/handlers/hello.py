"""simple dispatch"""
from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text

from src.client import formatter
from src.client import gettext as _
from src.handlers.keyboards import KeyboardSet

dp = Dispatch()


@dp.message(Text("/start"))
async def start(message: Message):
    await message.answer(
        formatter(_("enrollment")).format(message.from_user.first_name, "MusicAlertBot"),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=KeyboardSet.KEYBOARD_MENU.get_markup(),
    )
