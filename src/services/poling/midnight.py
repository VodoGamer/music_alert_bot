import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.services.poling.albums import albums_poling
from src.services.poling.notifications import notifications_polling


async def midnight_sync():
    while True:
        now = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        midnight = now.replace(hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
        wait_seconds = (midnight - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await albums_poling()
        await asyncio.sleep(1)
        await notifications_polling()
