from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PdfDocumentBase(BaseModel):
    file_name: str
    total_pages: int = 0


class PdfDocumentCreate(PdfDocumentBase):
    user_id: int
    file_path: str
    file_size: int = 0


class PdfDocumentUpdate(BaseModel):
    is_indexed: Optional[bool] = None
    faiss_index_path: Optional[str] = None
    chunk_count: Optional[int] = None
    total_pages: Optional[int] = None


class PdfDocumentOut(PdfDocumentBase):
    id: int
    user_id: int
    file_path: str
    file_size: int
    upload_date: datetime
    is_indexed: bool
    chunk_count: int

    model_config = {"from_attributes": True}
