from fastapi import APIRouter

from app.api.routers.authentication import router as authentication_router


api_router = APIRouter()

api_router.include_router(authentication_router)
