from groq import Groq

client = Groq(api_key="***REMOVIDO***")

# ── STT ──────────────────────────────────────────────
print("Testando STT...")
with open("./orpheus-english.wav", "rb") as f:
    transcription = client.audio.transcriptions.create(
        file=("./orpheus-english.wav", f.read()),
        model="whisper-large-v3-turbo",
        language="en",
    )

print("Transcrição:", transcription.text)