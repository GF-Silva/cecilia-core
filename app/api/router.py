from fastapi import APIRouter
from features.assistant.routes import router as assistant_router
from integrations.audio.routes import router as audio_router

api_router = APIRouter()

api_router.include_router(assistant_router, prefix="/assistant")
api_router.include_router(audio_router, prefix="/audio")