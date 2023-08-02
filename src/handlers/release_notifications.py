from yandex_music import Album, Artist

from src.client import api, formatter, gettext


async def send_release_notification_to_user(user_id: int, release: Album, artist: Artist):
    await api.send_message(
        chat_id=user_id,
        text=formatter(gettext("release_notification")).format(
            artist.name, ", ".join(release.artists_name()), release.title
        ),
        parse_mode=formatter.PARSE_MODE,
    )
