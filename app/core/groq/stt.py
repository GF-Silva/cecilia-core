from app.core.groq.client import client

class STT:
    def __init__(self):
        self.stt_client = client
        self.model = "whisper-large-v3-turbo"
    
    async def transcribe(self, file: str):
        print("Testando STT...")
        with open(file, "rb") as f:
            transcription = await client.audio.transcriptions.create(
                file=(file, f.read()),
                model=self.model,
                language="pt",
            )

        print("Transcrição:", transcription.text)
        return transcription.text