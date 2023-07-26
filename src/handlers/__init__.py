"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import add_performer, hello

dps: Iterable["Dispatch"] = (hello.dp, add_performer.dp)
