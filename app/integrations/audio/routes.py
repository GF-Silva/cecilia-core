from fastapi import APIRouter
from .wake_word import WakeWord

router = APIRouter()

wakeword = WakeWord()

@router.post("/run")
def run():
    wakeword.start()