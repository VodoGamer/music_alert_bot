from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataEq, CallbackDataMarkup
from telegrinder.types import InputFile

from src.client import api, dispatch, gettext, logger
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
        return logger.error(f"{event=}")
    await api.edit_message_text(
        chat_id=event.message.chat.id,
        message_id=event.message.message_id,
        text=gettext("request_performer_nickname"),
    )
    answer, _ = await dispatch.message.wait_for_message(event.message.chat.id)
    if not answer.text:
        return logger.error(f"{answer=}")
    performers = await search_performers(answer.text)
    if not performers:
        return await api.send_message(
            chat_id=answer.chat.id, text=gettext("performer_doesnt_exist")
        )
    performer = performers[0]
    if not performer.name:
        await api.send_message(chat_id=answer.chat.id, text=gettext("performer_doesnt_exist"))
    elif not performer.cover:
        await api.send_message(
            chat_id=answer.chat.id,
            text=gettext("best_result_of_performer_search").format(performer.name),
            reply_markup=get_correct_or_no_kb(performer.id),
        )
    else:
        await api.send_photo(
            answer.chat.id,
            caption=gettext("best_result_of_performer_search").format(performer.name),
            photo=InputFile(performer.name, await download_performer_cover(performer.cover)),
            reply_markup=get_correct_or_no_kb(performer.id),
        )


@dp.callback_query(CallbackDataMarkup("correct/yes/<performer_id>"))
async def correct_performer(event: CallbackQuery, performer_id: int):
    performer = await get_performer_by_id(performer_id)
    if not performer or not performer.name or not event.message:
        return logger.error(f"{performer_id=} {performer=} {event=}")
    await add_performer_to_user(event.from_user.id, int(performer.id), performer.name)

    await api.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
    await api.send_message(
        chat_id=event.message.chat.id,
        text=gettext("user_select_new_performer").format(performer.name),
    )


@dp.callback_query(CallbackDataEq("correct/no"))
async def wrong_performer(event: CallbackQuery):
    if not event.message:
        return logger.debug(f"{event=}")
    await api.edit_message_text(
        chat_id=event.message.chat.id, text=gettext("wrong_performer_search")
    )
