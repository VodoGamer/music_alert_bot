from enum import Enum

import redis.asyncio as redis

from src.config.env import REDIS_HOST


class State(Enum):
    WaitArtistNickname = "WaitArtistNickname"


connection = redis.Redis(host=REDIS_HOST, decode_responses=True)


async def set_state(user_id: int, state: State):
    await connection.set(str(user_id), state.value)


async def get_state(user_id: int) -> State | None:
    response = await connection.get(str(user_id))
    if response:
        return State(response)


async def remove_state(user_id: int):
    await connection.delete(str(user_id))
