from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq

from src.client import api, logger
from src.services.db.users import get_user_performers

dp = Dispatch()


@dp.callback_query(CallbackDataEq("menu/list_performers"))
async def list_performers(event: CallbackQuery):
    if not event.message:
        return logger.debug(f"{event=}")
    performers = await get_user_performers(event.from_user.id)
    performers_output = [performer.nickname for performer in performers]
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text="\n".join(performers_output),
    )
