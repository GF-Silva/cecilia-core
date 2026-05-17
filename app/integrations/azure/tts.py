import azure.cognitiveservices.speech as speechsdk
from .configs import tts_config
from core.queues import llm_stream_queue
from core.events import tts_running, llm_responding
from core.constrants import LLM_STOP_SIGNAL
import asyncio

class TTS:
    def __init__(self):
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_config)
        self.LLM_STOP_SIGNAL = object()
        
    async def run(self):
        tts_running.set() # define que o tts está rodando

        while True:
            await llm_responding.wait()

            # ─── 2. CRIAR O REQUEST ───────────────────────────────────────────────────────
            tts_request = speechsdk.SpeechSynthesisRequest(
                input_type=speechsdk.SpeechSynthesisRequestInputType.TextStream
            )

            tts_task = self.synthesizer.speak_async(tts_request)
        
            while not llm_stream_queue.empty() or llm_responding.is_set():
                chunk = await llm_stream_queue.get()
                if chunk == LLM_STOP_SIGNAL: break
                tts_request.input_stream.write(chunk)
                llm_stream_queue.task_done()
            
            tts_request.input_stream.close()
            await asyncio.to_thread(tts_task.get)