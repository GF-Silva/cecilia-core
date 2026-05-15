from integrations.azure.stt import STT
from integrations.groq.llm import LLM
from integrations.azure.tts import TTS
from core.queues import llm_stream_queue
import asyncio

class Assistant:
    def __init__(self):
        self.llm = LLM()
        self.stt = STT()
        self.tts = TTS()
    
    async def start(self):
        asyncio.create_task(self.llm.run())
        asyncio.create_task(self.stt.run())
        asyncio.create_task(self.tts.run())
    
    def get_context(self):
        return self.llm.context

    async def stream_prompt(self, contents: str):
        return await self.llm.stream_completion(contents=contents, queue=llm_stream_queue)