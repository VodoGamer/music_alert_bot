from yandex_music import Album

from src.client import api


async def send_release_notification_to_user(user_id: int, release: Album):
    await api.send_message(chat_id=user_id, text=f"{release.title}")
