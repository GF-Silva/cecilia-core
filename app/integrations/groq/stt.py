from .client import client
from core.queues import audio_queue, text_queue

class STT:
    def __init__(self):
        self.model = "whisper-large-v3-turbo"
        self.print_prefix = "STT"
    
    async def transcribe(self, audio_bytes):
        transcription = await client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model=self.model,
            language="pt",
        )

        print(f"{self.print_prefix}: Transcrição - ", transcription.text)
        return transcription.text

    async def process_audio(self):
        while True:
            audio = await audio_queue.get()
            transcription = await self.transcribe(audio)
            await text_queue.put(transcription)
            audio_queue.task_done()