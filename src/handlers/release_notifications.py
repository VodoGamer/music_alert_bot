from telegrinder.types import InputFile
from yandex_music import Album, Artist
from yandex_music.exceptions import TimedOutError

from src.client import api, formatter, gettext
from src.handlers.keyboards import get_release_link_kb


async def send_release_notification_to_user(user_id: int, release: Album, artist: Artist):
    try:
        cover = await release.download_cover_bytes_async("m1000x1000")
    except TimedOutError:
        await api.send_message(
            chat_id=user_id,
            text=formatter(gettext("release_notification")).format(
                artist.name, ", ".join(release.artists_name()), release.title
            ),
            parse_mode=formatter.PARSE_MODE,
            reply_markup=get_release_link_kb(release),
        )
        return
    await api.send_photo(
        chat_id=user_id,
        photo=InputFile(release.title or "new_release", cover),
        caption=formatter(gettext("release_notification")).format(
            artist.name, ", ".join(release.artists_name()), release.title
        ),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=get_release_link_kb(release),
    )
