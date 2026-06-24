from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal, engine
from app.models.user import User


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.email == "admin@documind.ai"))
        admin = result.scalar_one_or_none()
        if admin is None:
            admin = User(
                fullname="System Admin",
                email="admin@documind.ai",
                password_hash=hash_password("Admin@123"),
                role="admin",
            )
            session.add(admin)
            await session.commit()
            print("Admin seeded: admin@documind.ai / Admin@123")
        else:
            print("Admin already exists.")


if __name__ == "__main__":
    asyncio.run(seed())
