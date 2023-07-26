"""bot init"""
from telegrinder import API, Dispatch, Telegrinder, Token

from src.config.env import TELEGRAM_TOKEN

dispatch = Dispatch()
api = API(token=Token(TELEGRAM_TOKEN))
bot = Telegrinder(api)
