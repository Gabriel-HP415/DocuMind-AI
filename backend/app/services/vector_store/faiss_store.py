from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np

from app.core.config import settings
from app.services.vector_store.embedder import embed_texts

logger = logging.getLogger(__name__)


class FaissStore:
    def __init__(self, index_dir: Path, document_id: int) -> None:
        self.index_dir = index_dir
        self.document_id = document_id
        self.index_path = index_dir / f"doc_{document_id}.index"
        self.meta_path = index_dir / f"doc_{document_id}.meta.json"
        self._index: faiss.IndexFlatIP | None = None
        self._texts: list[str] = []
        self._load()

    def _load(self) -> None:
        if self.index_path.exists() and self.meta_path.exists():
            self._index = faiss.read_index(str(self.index_path))
            with open(self.meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            self._texts = meta.get("texts", [])

    def _persist(self) -> None:
        if self._index is None:
            return
        self.index_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump({"texts": self._texts}, f, ensure_ascii=False)

    def add_texts(self, texts: list[str]) -> None:
        logger.info(f"add_texts called with {len(texts)} texts for doc {self.document_id}")
        if not texts:
            logger.warning("No texts provided to add_texts")
            return
        embeddings = embed_texts(texts)
        logger.info(f"Generated {len(embeddings) if embeddings else 0} embeddings")
        if not embeddings:
            logger.error("embed_texts returned empty result")
            return
        vectors = np.array(embeddings, dtype="float32")
        logger.info(f"Vector shape: {vectors.shape}")
        if self._index is None:
            dim = vectors.shape[1]
            logger.info(f"Creating new FAISS index with dimension {dim}")
            self._index = faiss.IndexFlatIP(dim)
        self._index.add(vectors)
        self._texts.extend(texts)
        logger.info(f"Calling _persist for doc {self.document_id}")
        self._persist()
        logger.info(f"FAISS index saved to {self.index_path}")

    def search(self, query: str, top_k: int = 4) -> List[Tuple[str, float]]:
        if self._index is None or self._index.ntotal == 0:
            return []
        q_vec = np.array(embed_texts([query]), dtype="float32")
        scores, indices = self._index.search(q_vec, min(top_k, self._index.ntotal))
        results: List[Tuple[str, float]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self._texts[int(idx)], float(score)))
        return results

    def delete(self) -> None:
        for path in (self.index_path, self.meta_path):
            if path.exists():
                os.remove(path)
        self._index = None
        self._texts = []
