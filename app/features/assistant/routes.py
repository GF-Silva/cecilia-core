from fastapi import APIRouter
from .client import assistant

router = APIRouter()

@router.get("/prompt")
async def prompt(compose: str):
    return await assistant.send_prompt(compose)

@router.post("/start")
async def start_pipeline():
    return await assistant.start()