import torch
from silero_vad import load_silero_vad
import os
os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"

class VAD:
    def __init__(self, recorder):
        self.model = load_silero_vad()
        self.SAMPLE_RATE = 16000
        self.FRAME_SIZE = 512  # obrigatório pro silero
        self.recorder = recorder

        self.audio_buffer = []
        self.silence_start = None
        self.SILENCE_TIMEOUT = 1.5 # segundos sem fala = pausa real
        self.speaking = False
        self.running = False

    def start(self, on_silence):
        self.on_silence = on_silence
        self.recorder.start_stream(self.callback)
    
    def stop(self):
        self.recorder.stop_stream()

    def callback(self, indata, frames, time, status):
        audio = torch.from_numpy(indata[:, 0].copy())
        prob = self.model(audio, self.SAMPLE_RATE).item()

        if prob > 0.4:  # 0-1, ajusta conforme necessário
            self.silence_start = None
            if not self.speaking:
                self.speaking = True
                print("começou a falar")
            self.audio_buffer.append(indata[:, 0].copy())
        else:
            if self.speaking:
                if self.silence_start is None:
                    self.silence_start = time.currentTime
                elif time.currentTime - self.silence_start > self.SILENCE_TIMEOUT:
                    self.speaking = False
                    self.silence_start = None
                    self.on_silence(self.audio_buffer)
                    self.audio_buffer.clear()