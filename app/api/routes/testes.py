from fastapi import APIRouter

from app.core import gen_engine

router = APIRouter()

@router.get('/teste')
async def call_teste():
    return await gen_engine.process_prompt("manda aquela do guns")