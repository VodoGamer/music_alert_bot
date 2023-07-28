"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import add_performer, hello, list_performers

dps: Iterable["Dispatch"] = (hello.dp, add_performer.dp, list_performers.dp)
