from pathlib import Path
from typing import Any

from asyncpg import Connection, Record, connect

from src.client import logger
from src.config.env import POSTGRES_CONNECT


class MyRecord(Record):
    def __getattr__(self, name):
        return self[name]


async def execute_query(query_filename: str, *args):
    db = await _get_db()
    query = await _get_query(query_filename)
    logger.debug(f"execute db operation: {query=} with {args=}")
    await db.execute(query, *args)


async def fetch(query_filename: str, *args) -> list[Any] | None:
    db = await _get_db()
    query = await _get_query(query_filename)
    logger.debug(f"fetch db operation: {query=} with {args=}")
    result = await db.fetch(query, *args)
    return result if result != [] else None


async def _get_query(file_name: str) -> str:
    with open(Path("src/queries/", file_name), "r") as f:
        text = f.read()
    return text


async def _get_db() -> Connection:
    return await connect(POSTGRES_CONNECT, record_class=MyRecord)
