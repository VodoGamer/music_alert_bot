from src.client import bot
from src.handlers.release_notifications import send_notification_of_multiple_releases
from src.services.db.albums import get_not_listened_albums
from src.services.db.users import get_all_users, listen_albums
from src.services.yandex.artists import get_albums


@bot.loop_wrapper.interval(seconds=60)
async def notifications_polling():
    users = await get_all_users()
    for user in users:
        new_albums = await get_not_listened_albums(user.id)
        if not new_albums:
            continue
        api_albums = await get_albums([album.id for album in new_albums])
        await send_notification_of_multiple_releases(user.id, api_albums)
        await listen_albums(user.id, new_albums)
