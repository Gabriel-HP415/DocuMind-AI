from __future__ import annotations

from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import settings


def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def chunk_pages(pages: List[str]) -> List[str]:
    combined = "\n\n".join(pages)
    return chunk_text(combined)
