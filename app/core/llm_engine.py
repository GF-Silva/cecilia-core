from pydantic import BaseModel
from dotenv import load_dotenv
from groq import AsyncGroq, DefaultAioHttpClient
import os

load_dotenv()

class EngineInput(BaseModel):
    llm_model: str

class LLMEngine:
    def __init__(self, config: EngineInput):
        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            http_client=DefaultAioHttpClient()
        )

        self.llm_model = config.llm_model
    
    async def process_prompt(self, contents):
        chat_completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You just speak in portuguese from brasil. You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": contents
                }
            ],
            model=self.llm_model,
        )

        return chat_completion.choices[0].message.content