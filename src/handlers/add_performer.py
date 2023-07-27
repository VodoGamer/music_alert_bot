from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq, CallbackDataMarkup
from telegrinder.types import InputFile

from src.client import api, dispatch
from src.handlers.keyboards import get_correct_or_no_kb
from src.services.db.users import add_performer_to_user
from src.services.yandex.performers import (
    download_performer_cover,
    get_performer_by_id,
    search_performers,
)

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
    performers = await search_performers(performer_nickname)
    if not performers:
        return await api.send_message(
            chat_id=answer.chat.id,
            text=(
                "😓 Мне не удалось найти такого исполнителя в Яндекс Музыке, попробуйте уточнить "
                "запрос"
            ),
        )
    performer = performers[0]
    if not performer.name or not performer.cover:
        return
    await api.send_photo(
        answer.chat.id,
        caption=f"лучший результат: исполнитель {performer.name}.\nЭто правильно?",
        photo=InputFile(performer.name, await download_performer_cover(performer.cover)),
        reply_markup=get_correct_or_no_kb(performer.id),
    )


@dp.callback_query(CallbackDataMarkup("correct/yes/<performer_id>"))
async def correct_performer(event: CallbackQuery, performer_id: int):
    performer = await get_performer_by_id(performer_id)
    if not performer or not performer.name or not event.message:
        return
    await add_performer_to_user(event.from_user.id, int(performer.id), performer.name)

    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await api.send_message(
        chat_id=event.message.chat.id,
        text=f"✨ Вы начали следить за релизами {performer.name}",
    )
