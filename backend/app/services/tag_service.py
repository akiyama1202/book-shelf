from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag import TagCreate


def list_tags(db: Session, user_id: int) -> list[Tag]:
    return list(db.scalars(select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)))


def create_tag(db: Session, user_id: int, tag_in: TagCreate) -> Tag:
    existing = db.scalar(select(Tag).where(Tag.user_id == user_id, Tag.name == tag_in.name))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="同じ名前のタグが既に存在します。",
        )

    tag = Tag(user_id=user_id, name=tag_in.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def _get_owned_tag(db: Session, user_id: int, tag_id: int) -> Tag:
    tag = db.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="タグが見つかりません。")
    return tag


def rename_tag(db: Session, user_id: int, tag_id: int, tag_in: TagCreate) -> Tag:
    tag = _get_owned_tag(db, user_id, tag_id)

    existing = db.scalar(
        select(Tag).where(Tag.user_id == user_id, Tag.name == tag_in.name, Tag.id != tag_id)
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="同じ名前のタグが既に存在します。",
        )

    tag.name = tag_in.name
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, user_id: int, tag_id: int) -> None:
    tag = _get_owned_tag(db, user_id, tag_id)
    db.delete(tag)
    db.commit()
