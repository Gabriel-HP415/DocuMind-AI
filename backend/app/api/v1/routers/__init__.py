from app.api.v1.routers import auth, chat, health, admin, pdf
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(pdf.router)
api_router.include_router(chat.router)
api_router.include_router(admin.router)
api_router.include_router(health.router)

__all__ = ["api_router"]
