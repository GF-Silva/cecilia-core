from fastapi import APIRouter
from features.assistant.routes import router as assistant_router

api_router = APIRouter()

api_router.include_router(assistant_router, prefix="/assistant")