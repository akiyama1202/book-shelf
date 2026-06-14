from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.book import Book
from app.models.tag import Tag
from app.schemas.book import BookCreate, BookUpdate

SORT_COLUMNS = {
    "title": Book.title,
    "author": Book.author,
    "created_at": Book.created_at,
    "rating": Book.rating,
}


def _resolve_tags(db: Session, user_id: int, tag_names: list[str]) -> list[Tag]:
    unique_names = list(dict.fromkeys(tag_names))
    if not unique_names:
        return []

    existing_tags = list(
        db.scalars(select(Tag).where(Tag.user_id == user_id, Tag.name.in_(unique_names)))
    )
    existing_by_name = {tag.name: tag for tag in existing_tags}

    tags = []
    for name in unique_names:
        tag = existing_by_name.get(name)
        if tag is None:
            tag = Tag(user_id=user_id, name=name)
            db.add(tag)
            existing_by_name[name] = tag
        tags.append(tag)
    return tags


def list_books(
    db: Session,
    user_id: int,
    search: str | None,
    sort_by: str,
    sort_order: str,
    page: int,
    page_size: int,
) -> tuple[list[Book], int]:
    stmt = select(Book).where(Book.user_id == user_id)

    if search:
        keyword = f"%{search}%"
        stmt = stmt.where(Book.title.ilike(keyword) | Book.author.ilike(keyword))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0

    column = SORT_COLUMNS[sort_by]
    order = column.asc() if sort_order == "asc" else column.desc()
    stmt = (
        stmt.options(selectinload(Book.tags))
        .order_by(order)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    items = list(db.scalars(stmt))
    return items, total


def _get_owned_book(db: Session, user_id: int, book_id: int) -> Book:
    book = db.scalar(
        select(Book)
        .options(selectinload(Book.tags))
        .where(Book.id == book_id, Book.user_id == user_id)
    )
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="書籍が見つかりません。")
    return book


def get_book(db: Session, user_id: int, book_id: int) -> Book:
    return _get_owned_book(db, user_id, book_id)


def create_book(db: Session, user_id: int, book_in: BookCreate) -> Book:
    book = Book(
        user_id=user_id,
        title=book_in.title,
        author=book_in.author,
        status=book_in.status,
        rating=book_in.rating,
        memo=book_in.memo,
        tags=_resolve_tags(db, user_id, book_in.tags),
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, user_id: int, book_id: int, book_in: BookUpdate) -> Book:
    book = _get_owned_book(db, user_id, book_id)

    book.title = book_in.title
    book.author = book_in.author
    book.status = book_in.status
    book.rating = book_in.rating
    book.memo = book_in.memo
    book.tags = _resolve_tags(db, user_id, book_in.tags)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, user_id: int, book_id: int) -> None:
    book = _get_owned_book(db, user_id, book_id)
    db.delete(book)
    db.commit()
