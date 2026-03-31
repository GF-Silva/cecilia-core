from .llm_engine import LLMEngine, EngineInput
from .configs import llm_params

class Assistant:
    def __init__(self):
        self.llm = LLMEngine(EngineInput(**llm_params))
        self.audio_reecorder = None
        self.speaker = None
        self.transcriber = None

    async def send_prompt(self, compose):
        return await self.llm.process_prompt(compose)