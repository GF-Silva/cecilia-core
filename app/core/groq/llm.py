from app.core.groq.client import client

class LLM:
    def __init__(self):
        self.llm_client = client
        self.llm_model = "openai/gpt-oss-120b"
    
    async def process_prompt(self, contents):
        chat_completion = await self.llm_client.chat.completions.create(
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
