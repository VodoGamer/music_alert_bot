from telegrinder import CallbackQuery
from telegrinder.bot.rules.callback_data import CallbackQueryRule


class CallbackHasMessageRule(CallbackQueryRule):
    async def check(self, event: CallbackQuery, ctx: dict) -> bool | None:
        if event.message:
            ctx.update({"message": event.message})
            return True
