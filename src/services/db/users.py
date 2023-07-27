from pathlib import Path

from asyncpg import Connection, connect

from src.client import logger
from src.config.env import POSTGRES_CONNECT


async def register_user(user_id: int):
    await _execute_query("add_user.sql", user_id)


async def register_performer(performer_id: int, performer_nickname: str):
    await _execute_query("add_performer.sql", performer_id, performer_nickname)


async def add_performer_to_user(user_id: int, performer_id: int, performer_nickname: str):
    await register_user(user_id)
    await register_performer(performer_id, performer_nickname)
    await _execute_query("add_performer_to_user.sql", user_id, performer_id)


async def _execute_query(query_filename: str, *args):
    db = await _get_db()
    query = await _get_query(query_filename)
    logger.debug(f"execute db operation: {query=} with {args=}")
    await db.execute(query, *args)


async def _get_db() -> Connection:
    return await connect(POSTGRES_CONNECT)


async def _get_query(file_name: str) -> str:
    with open(Path("src/queries/", file_name), "r") as f:
        text = f.read()
    return text
