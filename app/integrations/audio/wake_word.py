import numpy as np
from openwakeword.model import Model
import openwakeword
import os
from .client import recorder, vad
import time

class WakeWord:
    def __init__(self):
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = 1280  # 80ms
        models_dir = os.path.join(os.path.dirname(openwakeword.__file__), "resources/models")
        model_path = os.path.join(models_dir, "hey_jarvis_v0.1.onnx")
        self.listen = True

        self.model = Model(wakeword_model_paths=[
            model_path
        ])

    def start(self):
        recorder.start_stream(self.callback)
        self.listen = True

        while self.listen:
            time.sleep(0.1)

        recorder.stop_stream()
        print("stop!")

        # Parou: chama o vad
        vad.start()

    def callback(self, indata, frames, time, status):
        audio = (indata[:, 0] * 32767).astype(np.int16)
        prediction = self.model.predict(audio)
        
        score = float(prediction["hey_jarvis_v0.1"])  # type: ignore

        if score > 0.4:
            print(f"hey jarvis! ({score:.2f})")
            self.listen = False