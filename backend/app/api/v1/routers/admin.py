from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.middleware.jwt import get_current_admin, get_current_user
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.pdf_repository import PdfRepository
from app.repositories.user_repository import UserRepository
from app.schemas.pdf_document import PdfDocumentOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def admin_list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    admin_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> list[UserOut]:
    repo = UserRepository(db)
    offset = (page - 1) * page_size
    users = await repo.list_all(limit=page_size, offset=offset)
    return [UserOut.model_validate(u) for u in users]


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> None:
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot delete themselves via this endpoint",
        )
    repo = UserRepository(db)
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.get("/documents/all", response_model=list[PdfDocumentOut])
async def admin_list_all_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    admin_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> list[PdfDocumentOut]:
    repo = PdfRepository(db)
    offset = (page - 1) * page_size
    docs = await repo.list_all(limit=page_size, offset=offset)
    return [PdfDocumentOut.model_validate(d) for d in docs]
