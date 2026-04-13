from core.queues import audio_queue
from silero_vad import load_silero_vad
import os
os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"
import torch
import asyncio
import numpy as np
import io
import wave

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
        self.print_prefix = "VAD"

    async def start(self):
        self.recorder.start_stream(self.callback)
    
    def build_wav(self, audio_buffer):
        if not audio_buffer:
            return

        audio = np.concatenate(audio_buffer)
        audio_int16 = (audio * 32767).astype(np.int16)

        # cria WAV válido em memória
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(audio_int16.tobytes())
        buf.seek(0)

        return buf

    def process_audio_chunk(self, audio: np.ndarray) -> np.ndarray:
        """
        Pipeline completo de filtros aplicado a cada chunk do microfone.
        Ordem importa: high-pass primeiro, depois gate, depois normalize.
        """
        audio = self.recorder.apply_high_pass(audio)
        audio = self.recorder.apply_noise_gate(audio)
        audio = self.recorder.apply_normalize(audio)
        return audio

    def callback(self, indata, frames, time, status):
        audio_np = self.process_audio_chunk(indata[:, 0].copy())
        audio = torch.from_numpy(audio_np)
        prob = self.model(audio, self.SAMPLE_RATE).item()

        if prob > 0.4:  # 0-1, ajusta conforme necessário
            self.silence_start = None
            if not self.speaking:
                self.speaking = True
                print(f"{self.print_prefix}: começou a falar")
            self.audio_buffer.append(indata[:, 0].copy())
        else:
            if not self.speaking:
                return
            
            if self.silence_start is None:
                self.silence_start = time.currentTime
            elif time.currentTime - self.silence_start > self.SILENCE_TIMEOUT:
                self.speaking = False
                self.silence_start = None
                
                print(f"{self.print_prefix}: parou de falar")
                audio_wav = self.build_wav(self.audio_buffer)
                asyncio.run(audio_queue.put(audio_wav))
                self.audio_buffer.clear()