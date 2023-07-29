"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import add_artist, hello, list_artists

dps: Iterable["Dispatch"] = (hello.dp, add_artist.dp, list_artists.dp)
