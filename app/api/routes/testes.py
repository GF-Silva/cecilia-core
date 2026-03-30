from fastapi import APIRouter

router = APIRouter()

@router.get('/teste')
def call_teste():
    return {
        "detail": "teste feito"
    }