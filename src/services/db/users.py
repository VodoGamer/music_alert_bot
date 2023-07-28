import ujson

from src.db import execute_query, fetch
from src.services.db.performers import Performer


async def register_user(user_id: int):
    await execute_query("add_user.sql", user_id)


async def register_performer(performer_id: int, performer_nickname: str):
    await execute_query("add_performer.sql", performer_id, performer_nickname)


async def add_performer_to_user(user_id: int, performer_id: int, performer_nickname: str):
    await register_user(user_id)
    await register_performer(performer_id, performer_nickname)
    await execute_query("add_performer_to_user.sql", user_id, performer_id)


async def get_user_performers(user_id: int) -> list[Performer]:
    performers = await fetch("get_user_performers.sql", user_id)
    return [Performer(**ujson.loads(performer[0])) for performer in performers]
