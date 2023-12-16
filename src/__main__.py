"""entry point"""
from src.client import bot, dispatch
from src.handlers import dps
from src.handlers.commands import set_bot_commands
from src.services.yandex.albums_poling import albums_auto_poling, albums_poling_by_time

for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.loop_wrapper.add_task(set_bot_commands())
bot.loop_wrapper.add_task(albums_auto_poling())
bot.loop_wrapper.add_task(albums_poling_by_time())
bot.run_forever()
