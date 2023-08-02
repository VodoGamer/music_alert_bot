"""entry point"""
import asyncio

from src.client import bot, dispatch, logger
from src.handlers import dps
from src.services.yandex.albums_poling import albums_poling

loop = asyncio.new_event_loop()
for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch = dispatch
loop.create_task(bot.run_polling())
loop.create_task(albums_poling())
try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt")
