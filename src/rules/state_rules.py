from telegrinder import Message, MessageRule

from src.services.states import State, get_state


class StateMessageRule(MessageRule):
    def __init__(self, state: State) -> None:
        self.state = state

    async def check(self, message: Message, ctx: dict) -> bool:
        return self.state == await get_state(message.from_user.id)

