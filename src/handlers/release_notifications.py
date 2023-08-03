from telegrinder.types import InputFile
from yandex_music import Album, Artist

from src.client import api, formatter, gettext
from src.services.yandex import download_cover


async def send_release_notification_to_user(user_id: int, release: Album, artist: Artist):
    cover = await download_cover(release.get_cover_url())
    await api.send_photo(
        chat_id=user_id,
        photo=InputFile(release.title or "new_release", cover),
        text=formatter(gettext("release_notification")).format(
            artist.name, ", ".join(release.artists_name()), release.title
        ),
        parse_mode=formatter.PARSE_MODE,
    )
