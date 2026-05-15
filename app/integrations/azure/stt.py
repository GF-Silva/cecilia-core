import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.audio as speechsdk_audio
from .configs import stt_config
from core.queues import transcription_queue
from core.events import stt_started, stt_stopped
import asyncio

class STT:
    def __init__(self):
        stt_config.speech_recognition_language = "pt-BR"
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=stt_config,
            audio_config=audio_config
        )
        self.print_prefix = "📄 STT"

    async def run(self):
        self.recognizer.recognized.connect(self.on_recognized)
        self.recognizer.speech_start_detected.connect(self.on_speech_start)
        self.recognizer.session_started.connect(self.on_start)
        self.recognizer.start_continuous_recognition_async()

        await stt_stopped.wait() # Espera até o stt parar
        self.recognizer.stop_continuous_recognition_async()

    def on_start(self, evt):
        print(f"{self.print_prefix} - Reconhecimento iniciado")
        stt_started.set() # Define q o stt comecou
    
    def on_speech_start(self, evt):
        print("Voz detectada")

    def on_recognized(self, evt: speechsdk.SpeechRecognitionEventArgs):
        if not evt.result.text: return
        print(f"{self.print_prefix} - Transcription: {evt.result.text}")
        asyncio.run(transcription_queue.put(evt.result.text))