from fastapi import APIRouter

from app.core import assistant

router = APIRouter()

@router.get('/teste')
async def call_teste(compose: str):
    return await assistant.send_prompt(compose)