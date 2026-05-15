import azure.cognitiveservices.speech as speechsdk
import re

# ─── 1. CONFIGURAÇÃO ──────────────────────────────────────────────────────────
speech_config = speechsdk.SpeechConfig(
    endpoint=f"wss://eastus.tts.speech.microsoft.com/cognitiveservices/websocket/v2",
    subscription="***REMOVIDO***"
)
speech_config.speech_synthesis_voice_name = "pt-BR-Macerio:DragonHDLatestNeural"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# ─── 2. CRIAR O REQUEST ───────────────────────────────────────────────────────
tts_request = speechsdk.SpeechSynthesisRequest(
    input_type=speechsdk.SpeechSynthesisRequestInputType.TextStream
)

tts_task = synthesizer.speak_async(tts_request)

text = "Oi, como posso te ajudar?"
text_tokens = ['Tudo', ' bem', ',', ' e', ' você', '?', ' Como', ' posso', ' ajudar', '?']
punctuation_marks = r'[.!?;:,—\-]|\.{3}'

buffer = ""
for chunk in text_tokens: # Simula a chegada de chunk
    if re.fullmatch(punctuation_marks, chunk):
        buffer += chunk
        print(buffer, end="\n", flush=True)
        tts_request.input_stream.write(buffer)
        buffer = ""
    else:
        buffer += chunk

# ─── 4. FECHAR E AGUARDAR ─────────────────────────────────────────────────────
tts_request.input_stream.close()
tts_task.get()

# print("\nPronto!")