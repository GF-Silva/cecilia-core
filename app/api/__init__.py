from fastapi import APIRouter
from .routes import testes

api_router = APIRouter()

api_router.include_router(testes.router)