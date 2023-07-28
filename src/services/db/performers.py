from pydantic import BaseModel


class Performer(BaseModel):
    id: int
    nickname: str
