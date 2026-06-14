from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.book import BookStatus
from app.schemas.tag import TagRead


class BookBase(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    status: BookStatus
    rating: int | None = Field(default=None, ge=1, le=5)
    memo: str | None = None
    tags: list[str] = []


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    status: BookStatus
    rating: int | None
    memo: str | None
    tags: list[TagRead]
    created_at: datetime
    updated_at: datetime


class BookListResponse(BaseModel):
    items: list[BookRead]
    total: int
    page: int
    page_size: int
