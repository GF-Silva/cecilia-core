import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

stt_config = speechsdk.SpeechConfig(
    subscription=os.getenv("AZURE_SPEECH_API_KEY"),
    region="eastus"
)

tts_config = speechsdk.SpeechConfig(
    endpoint="wss://eastus.tts.speech.microsoft.com/cognitiveservices/websocket/v2",
    subscription=os.getenv("AZURE_SPEECH_API_KEY")
)
tts_config.speech_synthesis_voice_name = "pt-BR-Thalita:DragonHDLatestNeural"