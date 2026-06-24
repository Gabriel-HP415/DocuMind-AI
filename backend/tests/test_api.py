from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


@pytest.mark.anyio
async def test_register_and_login_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        register_payload = {
            "fullname": "Test User",
            "email": "test@example.com",
            "password": "TestPass123!",
        }
        resp = await client.post("/api/v1/auth/register", json=register_payload)
        assert resp.status_code == 201
        user = resp.json()
        assert user["email"] == "test@example.com"

        login_payload = {"email": "test@example.com", "password": "TestPass123!"}
        resp = await client.post("/api/v1/auth/login", json=login_payload)
        assert resp.status_code == 200
        token_data = resp.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
