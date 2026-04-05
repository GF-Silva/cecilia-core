from fastapi import APIRouter
from .routes import testes, transcribe

api_router = APIRouter()

api_router.include_router(testes.router)
api_router.include_router(transcribe.router)