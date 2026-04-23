import azure.cognitiveservices.speech as speechsdk
from core.queues import transcription_queue
import asyncio

class STT:
    def __init__(self):
        speech_config = speechsdk.SpeechConfig(
            subscription="***REMOVIDO***",
            region="brazilsouth"
        )

        speech_config.speech_recognition_language = "pt-BR"

        audio_config = speechsdk.AudioConfig(use_default_microphone=True)

        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        self.print_prefix = "📄 STT"
        self.running = False

    async def run(self):
        self.recognizer.recognized.connect(self.on_recognized)
        self.recognizer.start_continuous_recognition_async()
        print(f"{self.print_prefix} - Reconhecimento iniciado")
        self.running = True

        while self.running:
            await asyncio.sleep(0.2)
        
        self.recognizer.stop_continuous_recognition_async()
        self.running = False

    def on_recognized(self, evt: speechsdk.SpeechRecognitionEventArgs):
        print(f"{self.print_prefix} - Transcription: {evt.result.text}")
        asyncio.run(transcription_queue.put(evt.result.text))