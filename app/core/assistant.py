from .groq.stt import STT
from .groq.llm import LLM

class Assistant:
    def __init__(self):
        self.llm = LLM()
        self.stt = STT()

    async def send_prompt(self, compose):
        return await self.llm.process_prompt(compose)

    async def transcribe(self, file: str):
        return await self.stt.transcribe(file)