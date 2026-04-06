import sounddevice as sd
import soundfile as sf
import numpy as np

# Grava o audio
class Recorder:
    def __init__(self, sample_rate, frame_size):
        self.SAMPLE_RATE = sample_rate
        self.frame_size = frame_size

    def start_stream(self, callback):
        print("start")
        self.stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=1,
            blocksize=self.frame_size,
            callback=callback
        )
        self.stream.start()
    
    def stop_stream(self):
        self.stream.stop()
        self.stream.close()

    def save_recording(self, audio_buffer):
        audio = np.concatenate(audio_buffer)
        sf.write("saida.wav", audio, self.SAMPLE_RATE)
        print("Salvo!")