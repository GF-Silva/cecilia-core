import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="***REMOVIDO***",
    region="brazilsouth"
)

speech_config.speech_recognition_language = "pt-BR"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def on_started(evt):
    print("🔊 TTS iniciado")

def on_completed(evt):
    print("✅ TTS concluído")

def on_word_boundary(evt):
    print(f"Palavra: {evt.text}")

synthesizer.synthesis_started.connect(on_started)
synthesizer.synthesis_completed.connect(on_completed)
synthesizer.synthesis_word_boundary.connect(on_word_boundary)

# não bloqueia
synthesizer.speak_text_async("Olá, eu sou o Suavio.")

# seu app continua aqui
while True:
    pass