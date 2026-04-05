from fastapi import APIRouter
from app.core import assistant

router = APIRouter()

@router.get("/transcribe")
async def transcribe(file):
    return await assistant.transcribe(file)