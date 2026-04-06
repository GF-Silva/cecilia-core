import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import openwakeword
import os

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms

models_dir = os.path.join(os.path.dirname(openwakeword.__file__), "resources/models")
model_path = os.path.join(models_dir, "hey_jarvis_v0.1.onnx")

model = Model(wakeword_model_paths=[
    model_path
])

def callback(indata, frames, time, status):
    audio = (indata[:, 0] * 32767).astype(np.int16)
    prediction = model.predict(audio)
    
    score = float(prediction["hey_jarvis_v0.1"])  # type: ignore

    if score > 0.4:
        print(f"hey jarvis! ({score:.2f})")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=CHUNK_SIZE, callback=callback):
    print("ouvindo...")
    input("Enter pra sair...")