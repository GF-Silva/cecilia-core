from .client import client
from core.queues import transcription_queue, response_queue
from groq.types.chat import ChatCompletionMessageParam
import asyncio

class LLM:
    def __init__(self):
        self.llm_client = client
        self.llm_model = "openai/gpt-oss-120b"
        self.print_prefix = "🤖 LLM"
        self.system_prompt = "Respond in Brazilian Portuguese. Be concise, like a natural conversation — 1 to 3 sentences unless more detail is asked. Never use markdown formatting like *, **, #, or similar characters."
        self.context: list[ChatCompletionMessageParam] = []
        self.max_context = 10

    async def run(self):
        while True:
            text = await transcription_queue.get()
            response = await self.process_prompt(text)
            print(f"{self.print_prefix} - Resposta: {response}")
            await response_queue.put(response)
            transcription_queue.task_done()
    
    async def process_prompt(self, contents):
        self.context.append({
            "role": "user",
            "content": contents
        })

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            *self.context[-self.max_context:] # Pega só os ultimos itens do context
        ]
        
        chat_completion = await self.llm_client.chat.completions.create(
            messages=messages,
            model=self.llm_model,
        )

        self.context.append({
            "role": "assistant",
            "content": chat_completion.choices[0].message.content
        })

        return chat_completion.choices[0].message.content
