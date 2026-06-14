from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.book import BookCreate, BookListResponse, BookRead, BookUpdate
from app.services.book_service import create_book, delete_book, get_book, list_books, update_book

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("", response_model=BookListResponse)
def get_books(
    search: str | None = None,
    sort_by: Literal["title", "author", "created_at", "rating"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookListResponse:
    items, total = list_books(db, current_user.id, search, sort_by, sort_order, page, page_size)
    return BookListResponse(
        items=[BookRead.model_validate(b) for b in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=BookRead, status_code=201)
def create(
    book_in: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookRead:
    return create_book(db, current_user.id, book_in)


@router.get("/{book_id}", response_model=BookRead)
def get(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookRead:
    return get_book(db, current_user.id, book_id)


@router.put("/{book_id}", response_model=BookRead)
def update(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookRead:
    return update_book(db, current_user.id, book_id, book_in)


@router.delete("/{book_id}", status_code=204)
def delete(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_book(db, current_user.id, book_id)
