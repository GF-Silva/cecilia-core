from .client import client

class STT:
    def __init__(self):
        self.model = "whisper-large-v3-turbo"
    
    async def transcribe(self, audio_bytes):
        print("Testando STT...")
        transcription = await client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model=self.model,
            language="pt",
        )

        print("Transcrição:", transcription.text)
        return transcription.text