from dataclasses import dataclass
from typing import Optional
import numpy as np
import pygame

@dataclass
class AudioData:
    audio_data: Optional[np.ndarray] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    duration: Optional[float] = None

    def __str__(self):
        parts = []
        if self.sample_rate is not None:
            parts.append(f"Sample rate: {self.sample_rate} Hz")
        if self.channels is not None:
            parts.append(f"Channels: {self.channels}")
        if self.duration is not None:
            parts.append(f"Duration: {self.duration:.2f} s")
        if self.audio_data is not None:
            parts.append(f"Data shape: {self.audio_data.shape}")
        if not parts:
            return "AudioData(empty)"
        return " | ".join(parts)


class AudioProcessor:
    def __init__(self):
        self.current_audio: Optional[AudioData] = None

    @staticmethod
    def get_audio_data(sound: pygame.mixer.Sound) -> AudioData:
        try:
            if not pygame.mixer.get_init():
                print("Pygame mixer not initialized.")

            raw_data = pygame.sndarray.array(sound)
            normalized_data = raw_data.astype(np.float32) / 32767.0

            if len(normalized_data.shape) == 1:
                channels = 1
            else:
                channels = normalized_data.shape[1]

            mixer_params = pygame.mixer.get_init()
            sample_rate = mixer_params[0] if mixer_params else 44100

            duration = sound.get_length()

            return AudioData(
                audio_data=normalized_data,
                sample_rate=sample_rate,
                channels=channels,
                duration=duration
            )

        except Exception as e:
            print(f"Error loading audio: {e}")
            return None

    def load_audio_file(self, file_path: str) -> bool:
            sound = pygame.mixer.Sound(file_path)
            if sound is None:
                return False
            
            self.current_audio = self.get_audio_data(sound)
            return True
        
    def get_waveform_chunk(self, start_sample: int, num_samples: int) -> Optional[np.ndarray]:
        if self.current_audio.audio_data is None:
            return None

        audio_data = self.current_audio.audio_data
        total_samples = audio_data.shape[0]

        if start_sample < 0:
            start_sample = 0
        
        if start_sample >= total_samples:
            return np.array([])

        end_sample = start_sample + num_samples
        
        if audio_data.ndim == 1: # Mono
            chunk = audio_data[start_sample:end_sample]
        elif audio_data.ndim == 2: # Stereo
            chunk = audio_data[start_sample:end_sample, :]
        else:
            return None
        
        return chunk
    
    def calculate_fft(self, start_sample: int, num_samples: int) -> Optional[tuple[np.ndarray, np.ndarray]]:

        if self.current_audio is None:
            return None

        sample_rate = self.current_audio.sample_rate
        if sample_rate is None or sample_rate <= 0:
            return None

        chunk = self.get_waveform_chunk(start_sample, num_samples)
        if chunk is None or chunk.size == 0:
            return None

        if chunk.ndim == 2 and chunk.shape[1] == 2:
            chunk_mono = chunk.mean(axis=1)
        else:
            chunk_mono = chunk.flatten()

        N = chunk_mono.shape[0]
        if N == 0:
            return None

        fft_result = np.fft.rfft(chunk_mono)
        mags = np.abs(fft_result)

        freqs = np.fft.rfftfreq(n=N, d=1.0 / sample_rate)

        return freqs, mags
    
    def get_audio_length_samples(self) -> int:
        return len(self.current_audio.audio_data) if self.current_audio.audio_data is not None else 0

    def get_sample_rate(self) -> int:
        return self.current_audio.sample_rate
    
    def get_current_sample_index(self) -> int:
        current_ms = pygame.mixer.music.get_pos()
        sample_rate = self.get_sample_rate()

        if sample_rate <= 0:
            return -1

        return int(current_ms / 1000.0 * sample_rate)