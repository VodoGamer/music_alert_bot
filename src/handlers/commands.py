from telegrinder.types import BotCommand

from src.client import api, gettext


async def set_bot_commands():
    await api.delete_my_commands()
    commands: list[BotCommand] = [
        BotCommand(command="/start", description=gettext("command_start")),
        BotCommand(command="/add_artist", description=gettext("command_add_artist")),
        BotCommand(command="/list", description=gettext("command_list")),
        BotCommand(command="/delete_artist", description=gettext("command_delete_artist")),
    ]
    await api.set_my_commands(commands=commands)
