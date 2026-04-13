import sounddevice as sd
import numpy as np
from scipy.signal import sosfilt, butter

# Grava o audio
class Recorder:
    def __init__(self, sample_rate, frame_size):
        self.SAMPLE_RATE = sample_rate
        self.frame_size = frame_size
        self.print_prefix = "RECORDER"
        self._HP_FILTER = self._make_high_pass(cutoff_hz=80, sample_rate=sample_rate)

    def start_stream(self, callback):
        print(f"{self.print_prefix}: start")
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
    
    def _make_high_pass(self, cutoff_hz: int, sample_rate: int):
        """
        Cria e retorna o filtro high-pass como SOS (Second-Order Sections).
        Chamado uma vez na inicialização — não recria a cada chunk.
        """
        sos = butter(N=4, Wn=cutoff_hz, btype='highpass', fs=sample_rate, output='sos')
        return sos

    def apply_high_pass(self, audio: np.ndarray) -> np.ndarray:
        """
        Remove frequências abaixo de 80Hz (rumble, ventilador, AC).
        Usa sosfilt que é numericamente estável para filtros de ordem alta.
        """
        result = sosfilt(self._HP_FILTER, audio)
        return np.asarray(result, dtype=np.float32)

    def apply_noise_gate(self, audio: np.ndarray, threshold: float = 0.015) -> np.ndarray:
        """
        Zera amostras abaixo do threshold de amplitude.
        Evita que ruído de fundo fraco seja enviado pro VAD/STT.

        threshold: valor entre 0.0 e 1.0 (áudio normalizado).
        0.015 é um bom ponto de partida — ajusta se cortar voz suave.
        """
        gated = audio.copy()
        gated[np.abs(gated) < threshold] = 0.0
        return gated

    def apply_normalize(self, audio: np.ndarray, target_peak: float = 0.9) -> np.ndarray:
        """
        Normaliza o pico do áudio para target_peak.
        Garante volume consistente pro Whisper independente do microfone.

        Ignora chunks quase silenciosos (pico < 1e-6) pra evitar divisão por zero.
        """
        peak = np.max(np.abs(audio))
        if peak < 1e-6:
            return audio
        return audio * (target_peak / peak)