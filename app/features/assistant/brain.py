from integrations.groq.stt import STT
from integrations.groq.llm import LLM
from integrations.audio.vad import VAD
from integrations.audio.recorder import Recorder
import asyncio

class Assistant:
    def __init__(self):
        self.SAMPLE_RATE = 16000
        FRAME_SIZE = 512  # obrigatório pro silero
        self.recorder = Recorder(self.SAMPLE_RATE, FRAME_SIZE)
        self.llm = LLM()
        self.stt = STT()
        self.vad = VAD(self.recorder)
        self.stt = STT()
    
    async def start(self):
        await asyncio.gather(
            self.vad.start(),
            self.stt.process_audio()
        )

    async def send_prompt(self, compose):
        return await self.llm.process_prompt(compose)

    async def transcribe(self, file: str):
        return await self.stt.transcribe(file)