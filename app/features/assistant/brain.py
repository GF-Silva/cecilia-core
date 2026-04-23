from integrations.azure.stt import STT
from integrations.groq.llm import LLM
import asyncio

class Assistant:
    def __init__(self):
        self.llm = LLM()
        self.stt = STT()
    
    async def start(self):
        asyncio.create_task(self.llm.run())
        asyncio.create_task(self.stt.run())
    
    def get_context(self):
        return self.llm.context

    async def send_prompt(self, compose):
        return await self.llm.process_prompt(compose)