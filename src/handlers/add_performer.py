from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq

from src.client import api, dispatch

dp = Dispatch()


@dp.callback_query(CallbackDataEq("menu/add_performer"))
async def add_performer(event: CallbackQuery):
    if not event.message:
        return
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text="Напишите псевдоним исполнителя: ",
    )
    answer, _ = await dispatch.message.wait_for_message(event.message.chat.id)
    if not answer.text:
        return
    artist_nickname = answer.text
