"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import hello

dps: Iterable["Dispatch"] = (hello.dp,)
