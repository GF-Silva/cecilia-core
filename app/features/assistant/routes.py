from fastapi import APIRouter
from .client import assistant

router = APIRouter()

@router.get("/prompt")
async def prompt(compose: str):
    return await assistant.send_prompt(compose)

@router.get("/context")
def get_context():
    return assistant.get_context()

@router.post("/start")
async def start():
    await assistant.start()
    return

@router.post("/stop")
def stop():
    assistant.stop()
    return