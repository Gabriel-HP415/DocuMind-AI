from __future__ import annotations

from functools import lru_cache
from typing import List

from langchain_ollama import OllamaEmbeddings

from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.OLLAMA_EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedding_model()
    return model.embed_documents(texts)
