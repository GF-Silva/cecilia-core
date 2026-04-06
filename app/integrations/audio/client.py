from .recorder import Recorder
from .vad import VAD

SAMPLE_RATE = 16000
FRAME_SIZE = 512  # obrigatório pro silero
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms

recorder = Recorder(SAMPLE_RATE, FRAME_SIZE)
vad = VAD()