from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.middleware.jwt import get_current_user
from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.pdf_repository import PdfRepository
from app.schemas.chat import ChatAskRequest, ChatAskResponse, ChatSessionOut
from app.services.rag import RagService
from app.services.vector_store import FaissStore

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatAskResponse)
async def ask(
    payload: ChatAskRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatAskResponse:
    pdf_repo = PdfRepository(db)
    chat_repo = ChatRepository(db)

    doc = await pdf_repo.get_by_id(payload.document_id)
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

    if not doc.is_indexed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document has not been indexed yet. Please re-upload or index it first.",
        )

    session_id = payload.session_id
    session = None
    if session_id is not None:
        session = await chat_repo.get_session(session_id)
        if session is None or session.user_id != current_user.id:
            session = None  # Tạo session mới
        elif session.document_id != doc.id:
            # Document khác → tạo session mới, xóa session cũ
            await chat_repo.delete_session(session_id)
            session = None

    if session is None:
        session = await chat_repo.create_session(
            ChatSession(
                user_id=current_user.id,
                document_id=doc.id,
                title=payload.question[:80],
            )
        )
    session_id = session.id

    await chat_repo.add_message(
        ChatMessage(
            session_id=session_id,
            sender="user",
            message=payload.question,
        )
    )

    try:
        faiss_store = FaissStore(settings.FAISS_INDEX_DIR, doc.id)
        rag = RagService(faiss_store)
        answer, sources = rag.ask(payload.question)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI processing failed: {exc}",
        ) from exc

    await chat_repo.add_message(
        ChatMessage(
            session_id=session_id,
            sender="assistant",
            message=answer,
            meta_json={"sources": sources, "document_id": doc.id},
        )
    )

    return ChatAskResponse(answer=answer, session_id=session_id, sources=sources)


@router.get("/history/{session_id}", response_model=list[dict])
async def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    chat_repo = ChatRepository(db)
    session = await chat_repo.get_session(session_id)
    if session is None or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )
    messages = await chat_repo.get_messages(session_id)
    return [
        {
            "id": msg.id,
            "sender": msg.sender,
            "message": msg.message,
            "created_at": msg.created_at.isoformat(),
            "meta": msg.meta_json,
        }
        for msg in messages
    ]


@router.get("/sessions", response_model=list[ChatSessionOut])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ChatSessionOut]:
    chat_repo = ChatRepository(db)
    sessions = await chat_repo.list_sessions_by_user(current_user.id)
    return [ChatSessionOut.model_validate(s) for s in sessions]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    chat_repo = ChatRepository(db)
    session = await chat_repo.get_session(session_id)
    if session is None or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )
    await chat_repo.delete_session(session_id)
