from yandex_music import ClientAsync

from src.client import yandex_client


class GetYandexApi:
    def __init__(self):
        self.api = None

    async def __call__(self) -> ClientAsync:
        if not self.api:
            self.api = await yandex_client.init()
        return self.api


get_yandex_api = GetYandexApi()
