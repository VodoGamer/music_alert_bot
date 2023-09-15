from telegrinder.types import InputFile
from yandex_music import Album, Artist
from yandex_music.exceptions import TimedOutError

from src.client import api, formatter, gettext
from src.handlers.keyboards import get_release_link_kb


def get_album_type(album: Album) -> str:
    if album.track_count == 1:
        return "сингл"
    elif album.track_count == 2:
        return "макси-сингл"
    elif album.track_count and album.track_count >= 3:
        return "сборник треков"
    else:
        return "релиз"


async def send_release_notification_to_user(user_id: int, release: Album, artist: Artist):
    notification_text = formatter(gettext("release_notification")).format(
        artist.name,
        ", ".join(release.artists_name()),
        release.title,
        release_type=get_album_type(release),
    )
    try:
        cover = await release.download_cover_bytes_async("m1000x1000")
    except TimedOutError:
        await api.send_message(
            chat_id=user_id,
            text=notification_text,
            parse_mode=formatter.PARSE_MODE,
            reply_markup=get_release_link_kb(release),
        )
        return
    await api.send_photo(
        chat_id=user_id,
        photo=InputFile(release.title or "new_release", cover),
        caption=notification_text,
        parse_mode=formatter.PARSE_MODE,
        reply_markup=get_release_link_kb(release),
    )
