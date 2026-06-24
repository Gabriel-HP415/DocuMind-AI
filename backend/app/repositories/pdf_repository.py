from __future__ import annotations

import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pdf_document import PdfDocument
from app.models.user import User


class PdfRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, doc_id: int) -> PdfDocument | None:
        result = await self.db.execute(
            select(PdfDocument).where(PdfDocument.id == doc_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int, limit: int = 20, offset: int = 0) -> list[PdfDocument]:
        result = await self.db.execute(
            select(PdfDocument)
            .where(PdfDocument.user_id == user_id)
            .order_by(PdfDocument.upload_date.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count_by_user(self, user_id: int) -> int:
        result = await self.db.execute(
            select(PdfDocument).where(PdfDocument.user_id == user_id)
        )
        return len(result.scalars().all())

    async def create(self, document: PdfDocument) -> PdfDocument:
        self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)
        return document

    async def update(self, document: PdfDocument) -> PdfDocument:
        await self.db.flush()
        await self.db.refresh(document)
        return document

    async def delete(self, doc_id: int) -> bool:
        document = await self.get_by_id(doc_id)
        if document is None:
            return False
        await self.db.delete(document)
        await self.db.flush()
        return True

    async def list_all(self, limit: int = 50, offset: int = 0) -> list[PdfDocument]:
        result = await self.db.execute(
            select(PdfDocument)
            .order_by(PdfDocument.upload_date.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
