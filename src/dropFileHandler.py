from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pygame

@dataclass
class MusicData:
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
            return "MusicData(empty)"
        return " | ".join(parts)



class DropFileHandler:
    def __init__(self):
        self.supported_formats = ['.mp3', '.wav']

    def handle_file(self, file_path: str) -> bool:
        suffix = Path(file_path).suffix.lower()
        return suffix in self.supported_formats

    def load_audio_file(self, file_path: str) -> Optional[MusicData]:
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

            return MusicData(
                audio_data=normalized_data,
                sample_rate=sample_rate,
                channels=channels,
                duration=duration
            )

        except Exception as e:
            print(f"Error loading audio: {e}")
            return None
