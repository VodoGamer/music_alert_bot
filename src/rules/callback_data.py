import typing
from contextlib import suppress

from telegrinder import CallbackQuery
from telegrinder.model import decoder
from telegrinder.rules import CallbackQueryDataRule


class CallbackDataJsonItemEq(CallbackQueryDataRule):
    def __init__(self, k: dict[str, typing.Any] | str, v: str | None = None):
        self.key = tuple(k.keys())[0] if isinstance(k, dict) else k
        self.value = k[self.key] if isinstance(k, dict) else v

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        with suppress(BaseException):
            return decoder.decode(event.data.unwrap(), type=dict)[self.key] == self.value
        return False
