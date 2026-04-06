from fastapi import APIRouter
from .client import assistant

router = APIRouter()

@router.post("/run")
async def run():
    return

@router.get("/prompt")
async def prompt(compose: str):

    return await assistant.send_prompt(compose)