from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatSessionBase(BaseModel):
    title: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    document_id: int


class ChatSessionOut(ChatSessionBase):
    id: int
    user_id: int
    document_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageBase(BaseModel):
    sender: str
    message: str


class ChatMessageCreate(ChatMessageBase):
    session_id: int


class ChatMessageOut(ChatMessageBase):
    id: int
    session_id: int
    meta_json: Optional[dict] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatAskRequest(BaseModel):
    document_id: int
    question: str
    session_id: Optional[int] = None


class ChatAskResponse(BaseModel):
    answer: str
    session_id: int
    sources: list[dict]
