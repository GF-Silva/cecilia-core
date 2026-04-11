from fastapi import APIRouter
import numpy as np
import io
import wave
from .vad import VAD
from .client import recorder
from integrations.groq.stt import STT
import asyncio

stt = STT()

SAMPLE_RATE = 16000
def build_wav(audio_buffer):
    if not audio_buffer:
        return

    audio = np.concatenate(audio_buffer)
    audio_int16 = (audio * 32767).astype(np.int16)

    # cria WAV válido em memória
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())
    buf.seek(0)

    return buf

def on_silence(audio_buffer):
    file = build_wav(audio_buffer)
    asyncio.run(stt.transcribe(file))

# TODO: Criar uma class para gerenciar tudo isso

router = APIRouter()
@router.post("/run")
async def run():
    vad = VAD(recorder)
    vad.start(on_silence)