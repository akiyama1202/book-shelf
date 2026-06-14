from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.tag import TagCreate, TagRead
from app.services.tag_service import create_tag, delete_tag, list_tags, rename_tag

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("", response_model=list[TagRead])
def get_tags(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[TagRead]:
    return list_tags(db, current_user.id)


@router.post("", response_model=TagRead, status_code=201)
def create(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TagRead:
    return create_tag(db, current_user.id, tag_in)


@router.put("/{tag_id}", response_model=TagRead)
def update(
    tag_id: int,
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TagRead:
    return rename_tag(db, current_user.id, tag_id, tag_in)


@router.delete("/{tag_id}", status_code=204)
def delete(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_tag(db, current_user.id, tag_id)
