from fastapi import APIRouter

from app.api.routers.authentication import router as authentication_router
from app.api.routers.users import router as users_router


api_router = APIRouter()

api_router.include_router(authentication_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
