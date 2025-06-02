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

    def load_audio_file(self, file_path: str) -> Optional[AudioData]:
        try:
            if not pygame.mixer.get_init():
                print("Pygame mixer not initialized.")
                return None

            sound = pygame.mixer.Sound(file_path)
            raw_data = pygame.sndarray.array(sound)
            normalized_data = raw_data.astype(np.float32) / 32767.0

            if len(normalized_data.shape) == 1:
                channels = 1
            else:
                channels = normalized_data.shape[1]

            mixer_params = pygame.mixer.get_init()
            sample_rate = mixer_params[0] if mixer_params else 44100

            duration = sound.get_length()

            self.current_audio = AudioData(
                audio_data=normalized_data,
                sample_rate=sample_rate,
                channels=channels,
                duration=duration
            )
            return self.current_audio

        except Exception as e:
            print(f"Error loading audio: {e}")
            return None
        

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