import pygame
from waveformRenderer import WaveformRenderer
from dragOverlay import DragOverlay
from dropFileHandler import DropFileHandler
from audioProcessor import AudioProcessor
from volumeOverlay import VolumeOverlay
from settings import Settings
import numpy as np

class Window():
    def __init__(self):
        self.width, self.height = (1200, 800)
        self.colors = {
            'bg': (128, 128, 128),
        }

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Audio Waveform Visualizer")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True

        self.file_handler = DropFileHandler()
        self.audio_processor = AudioProcessor()
        self.wave_renderer = WaveformRenderer(self.width, self.height)
        self.drag_overlay = DragOverlay(self.width, self.height)
        self.volume_overlay = VolumeOverlay()

        self.freqs = None
        self.mags = None
        self.audio_length_samples = 0

    def update(self):
        while self.running:
            self.handle_events()
            self.update_fft_data()

            self.screen.fill(self.drag_overlay.get_background_color(self.colors['bg']))

            self.wave_renderer.draw_grid(self.screen)

            if self.freqs is not None and self.mags is not None:
                self.wave_renderer.draw_waveform_fft(self.screen, self.freqs, self.mags)

            self.drag_overlay.draw_hover_overlay(self.screen)
            self.volume_overlay.draw_volume_bar(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    
    def update_fft_data(self): # Consider refactor
       if Settings.is_playing and pygame.mixer.music.get_busy():
                current_ms = pygame.mixer.music.get_pos()
                sample_rate = self.audio_processor.get_sample_rate()

                if sample_rate > 0 and self.audio_length_samples > 0:
                    current_sample_index = int(current_ms / 1000.0 * sample_rate)

                    if current_sample_index < self.audio_length_samples:
                        freqs_mags = self.audio_processor.calculate_fft(
                            start_sample=current_sample_index,
                            num_samples=Settings.fft_window_size
                        )

                        if freqs_mags is not None:
                            self.freqs, self.mags = freqs_mags


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.drag_overlay.handle_event(event)
            self.volume_overlay.handle_event(event)

            if event.type == pygame.DROPFILE:
                if Settings.is_playing:
                    pygame.mixer.music.stop()
                    Settings.is_playing = False

                if self.file_handler.handle_file(event.file):
                    if self.audio_processor.load_audio_file(event.file):
                        self.audio_length_samples = self.audio_processor.get_audio_length_samples()
                        Settings.is_playing = True
                        pygame.mixer.music.play()

            self.handle_key_down_event(event)

    def handle_key_down_event(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Settings.is_playing:
                    pygame.mixer.music.pause()
                    Settings.is_playing = False
                elif pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() > 0:
                    pygame.mixer.music.unpause()
                    Settings.is_playing = True
