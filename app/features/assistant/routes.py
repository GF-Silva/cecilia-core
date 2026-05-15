from fastapi import APIRouter
from .client import assistant
from integrations.groq.llm import LLM

router = APIRouter()

@router.get("/prompt-stream")
async def prompt_stream(compose: str):
    return await assistant.stream_prompt(compose)

@router.get("/get-context")
def get_context():
    return assistant.get_context()

@router.post("/start")
async def start():
    return await assistant.start()