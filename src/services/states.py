from enum import Enum

import redis.asyncio as redis


class State(Enum):
    WaitArtistNickname = "WaitArtistNickname"


connection = redis.Redis(decode_responses=True)


async def set_state(user_id: int, state: State):
    await connection.set(str(user_id), state.value)


async def get_state(user_id: int) -> State:
    return State(await connection.get(str(user_id)))

