"""entry point"""
from src.client import bot, dispatch
from src.handlers import dps
from src.handlers.commands import set_bot_commands
from src.services.poling.albums import albums_poling
from src.services.poling.midnight import midnight_sync
from src.services.poling.notifications import notifications_polling

for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.loop_wrapper.on_startup.append(set_bot_commands())
bot.loop_wrapper.add_task(albums_poling)
bot.loop_wrapper.add_task(notifications_polling)
bot.loop_wrapper.add_task(midnight_sync)
bot.run_forever()
