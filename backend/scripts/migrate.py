#!/usr/bin/env python3
"""One-time database migration: create all tables."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.db.session import Base, engine
from app.models.user import User
from app.models.pdf_document import PdfDocument
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


async def create_tables():
    async with engine.begin() as conn:
        # Drop all tables first (safe for dev — data will be lost)
        await conn.run_sync(Base.metadata.drop_all)
        print("Dropped existing tables.")
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Created tables: users, pdf_documents, chat_sessions, chat_messages")


if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Migration complete.")
