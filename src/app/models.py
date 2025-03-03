from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def datetime_now_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000000)


class Article(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    updated_at: str = Field(default_factory=lambda: str(datetime_now_timestamp()))
    headline: str
    body: str
    thumbnail_image: str | None
