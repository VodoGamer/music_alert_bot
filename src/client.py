"""bot init"""
from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.tools import HTMLFormatter

from src.config.env import TELEGRAM_TOKEN

formatter = HTMLFormatter
dispatch = Dispatch()
api = API(token=Token(TELEGRAM_TOKEN))
bot = Telegrinder(api)
