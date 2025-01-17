# Application entry point
from app.api.internal import admin
from app.api.routes import heroes, items, notifications, users
from app.api.routes.auth import login
from app.static import files
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(items.router)
api_router.include_router(users.router)
api_router.include_router(heroes.router)
api_router.include_router(login.router)
api_router.include_router(files.router)
api_router.include_router(notifications.router)
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
