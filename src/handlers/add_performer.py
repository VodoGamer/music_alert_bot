from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq, CallbackDataMarkup
from telegrinder.types import InputFile

from src.client import api, dispatch
from src.handlers.keyboards import get_correct_or_no_kb
from src.services.yandex.performers import get_performer_info

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
    performer_nickname = answer.text
    performer = await get_performer_info(performer_nickname)
    if performer and performer.cover:
        # TODO: handle case when performer or their cover is not found
        await api.send_photo(
            answer.chat.id,
            caption=f"лучший результат: исполнитель {performer.nickname}.\nЭто правильно?",
            photo=InputFile(performer.nickname, performer.cover),
            reply_markup=get_correct_or_no_kb(performer.nickname),
        )


@dp.callback_query(CallbackDataMarkup("correct/yes/<nickname>"))
async def correct_performer(event: CallbackQuery, nickname: str):
    if not event.message:
        return
    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await api.send_message(
        chat_id=event.message.chat.id,
        text=f"✨ Вы начали следить за релизами {nickname}",
    )
