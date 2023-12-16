"""bot init"""
import gettext
from pathlib import Path

from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.tools import HTMLFormatter
from yandex_music import ClientAsync

from src.config.env import TELEGRAM_TOKEN

gnu_translations = gettext.translation(
    domain="messages", localedir=Path("locale"), languages=["ru_RU"]
)
gettext = gnu_translations.gettext

logger = logger
formatter = HTMLFormatter
dispatch = Dispatch()
api = API(token=Token(TELEGRAM_TOKEN))
bot = Telegrinder(api=api, dispatch=dispatch)

yandex_client = ClientAsync()
