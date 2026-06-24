from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import List

from pypdf import PdfReader

from app.core.config import settings


def compute_file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def save_upload_file(upload_file_path: str, dest_dir: Path) -> str:
    dest_dir.mkdir(parents=True, exist_ok=True)
    file_hash = compute_file_hash(upload_file_path)
    source = Path(upload_file_path)
    ext = source.suffix or ".pdf"
    dest_name = f"{file_hash}{ext}"
    dest_path = dest_dir / dest_name
    if not dest_path.exists():
        os.replace(upload_file_path, str(dest_path))
    else:
        os.remove(upload_file_path)
    return str(dest_path)


def extract_text_from_pdf(file_path: str) -> List[str]:
    reader = PdfReader(file_path)
    pages_text: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)
    return pages_text
