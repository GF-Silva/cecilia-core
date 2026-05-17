from .client import client
from core.queues import transcription_queue, llm_stream_queue
from core.events import llm_running, llm_responding
from groq.types.chat import ChatCompletionMessageParam
from core.constrants import LLM_STOP_SIGNAL
import asyncio
import re

class LLM:
    def __init__(self):
        self.llm_client = client
        self.llm_model = "openai/gpt-oss-120b"
        self.print_prefix = "🤖 LLM"
        self.system_prompt = "Respond in Brazilian Portuguese. Be concise, like a natural conversation — 1 to 3 sentences unless more detail is asked. Never use markdown formatting like *, **, #, or similar characters."
        self.context: list[ChatCompletionMessageParam] = []
        self.max_context = 10
        self.punctuation_regex = r'[.!?;:,—\-]|\.{3}'

    async def run(self):
        llm_running.set() # Define que comecou

        # Enquanto estiver rodando, consome as transcription
        while llm_running.is_set():
            text = await transcription_queue.get()
            await self.stream_completion(contents=text, queue=llm_stream_queue)
            transcription_queue.task_done()

    async def stream_completion(self, queue: asyncio.Queue, contents: str):
        try:
            self.context.append({
                "role": "user",
                "content": contents
            })

            messages: list[ChatCompletionMessageParam] = [
                {"role": "system", "content": self.system_prompt},
                *self.context[-self.max_context:] # Pega só os ultimos itens do context
            ]

            stream = await client.chat.completions.create(
                messages=messages,
                model=self.llm_model,
                stream=True,
            )

            response = ""
            stream_buffer = ""
            first_chunk = True
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if first_chunk: first_chunk = False; llm_responding.set()

                if not content or not isinstance(content, str): continue
                
                if re.fullmatch(self.punctuation_regex, content):
                    stream_buffer += content
                    await queue.put(stream_buffer)
                    stream_buffer = ""
                    continue
                
                stream_buffer += content
                response += content
            
            llm_responding.clear()
            await queue.put(LLM_STOP_SIGNAL)
            self.context.append({
                "role": "assistant",
                "content": response
            })

            print(f"{self.print_prefix} - Response: {response}")
            return response
        
        except Exception as e:
            print(f"{self.print_prefix} - Erro: {e}")