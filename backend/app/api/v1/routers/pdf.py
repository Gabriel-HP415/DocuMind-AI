from __future__ import annotations

import datetime
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.db.session import get_db
from app.middleware.jwt import get_current_user
from app.models.pdf_document import PdfDocument
from app.models.user import User
from app.repositories.pdf_repository import PdfRepository
from app.schemas.pdf_document import PdfDocumentCreate, PdfDocumentOut
from app.services.pdf_processor import (
    chunk_pages,
    extract_text_from_pdf,
    save_upload_file,
)
from app.services.vector_store import FaissStore

router = APIRouter(prefix="/documents", tags=["pdf"])


def _build_pdf_document_create(
    user_id: int, file_name: str, file_path: str, file_size: int, total_pages: int
) -> PdfDocumentCreate:
    return PdfDocumentCreate(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        file_size=file_size,
        total_pages=total_pages,
    )


@router.post("/upload-pdf", response_model=PdfDocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PdfDocumentOut:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    tmp_path = settings.UPLOAD_DIR / f"tmp_{file.filename}"
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size is {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    with open(tmp_path, "wb") as f:
        f.write(content)

    try:
        dest_path = save_upload_file(str(tmp_path), settings.UPLOAD_DIR)
        pages = extract_text_from_pdf(dest_path)
        total_pages = len(pages)

        repo = PdfRepository(db)
        doc_create = _build_pdf_document_create(
            user_id=current_user.id,
            file_name=file.filename,
            file_path=dest_path,
            file_size=len(content),
            total_pages=total_pages,
        )
        doc = PdfDocument(**doc_create.model_dump())
        document = await repo.create(doc)

        chunks = chunk_pages(pages)
        faiss_store = FaissStore(settings.FAISS_INDEX_DIR, document.id)
        faiss_store.add_texts(chunks)

        document.is_indexed = True
        document.chunk_count = len(chunks)
        document.faiss_index_path = str(settings.FAISS_INDEX_DIR / f"doc_{document.id}.index")
        await repo.update(document)

        return PdfDocumentOut.model_validate(document)
    except Exception as exc:
        # cleanup on failure
        if tmp_path.exists():
            tmp_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process PDF: {exc}",
        ) from exc


@router.get("/", response_model=list[PdfDocumentOut])
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[PdfDocumentOut]:
    repo = PdfRepository(db)
    offset = (page - 1) * page_size
    docs = await repo.get_by_user(current_user.id, limit=page_size, offset=offset)
    return [PdfDocumentOut.model_validate(doc) for doc in docs]


@router.get("/all", response_model=list[PdfDocumentOut])
async def list_all_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: AsyncSession = Depends(get_db),
) -> list[PdfDocumentOut]:
    repo = PdfRepository(db)
    offset = (page - 1) * page_size
    docs = await repo.list_all(limit=page_size, offset=offset)
    return [PdfDocumentOut.model_validate(doc) for doc in docs]


@router.get("/{document_id}", response_model=PdfDocumentOut)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PdfDocumentOut:
    repo = PdfRepository(db)
    doc = await repo.get_by_id(document_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    if doc.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this document",
        )
    return PdfDocumentOut.model_validate(doc)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    repo = PdfRepository(db)
    doc = await repo.get_by_id(document_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    if doc.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this document",
        )

    # Remove FAISS index
    try:
        store = FaissStore(settings.FAISS_INDEX_DIR, document_id)
        store.delete()
    except Exception:
        pass

    await repo.delete(document_id)
