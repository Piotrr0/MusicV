import pygame
from waveformRenderer import WaveformRenderer
from dragOverlay import DragOverlay
from dropFileHandler import DropFileHandler
from audioProcessor import AudioProcessor
from volumeOverlay import VolumeOverlay
from settings import Settings
from youtubeHandler import YoutubeHandler
from titleOverlay import TitleOverlay
import pyperclip
import threading

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
        self.title_overlay = TitleOverlay(self.width, self.height)
        self.volume_overlay = VolumeOverlay(self.width)
        self.youtubeHandler = YoutubeHandler()

        self.freqs = None
        self.mags = None
        self.audio_length_samples = 0

        self.fft_lock = threading.Lock()
        self.fft_worker_running = False
        self.stop_fft_thread = threading.Event()

    def update(self):
        while self.running:
            self.handle_events()
            self.update_fft_data()

            self.draw_gui()

            pygame.display.flip()
            self.clock.tick(60)

        self.stop_fft_thread.set()
        pygame.quit()
    
    def draw_gui(self):
        self.screen.fill(self.drag_overlay.get_background_color(self.colors['bg']))
            
        self.wave_renderer.draw_grid(self.screen)

        with self.fft_lock:
            freqs = None if self.freqs is None else self.freqs.copy()
            mags = None if self.mags is None else self.mags.copy()

        if freqs is not None and mags is not None:
            self.wave_renderer.draw_waveform_fft(self.screen, freqs, mags)

        self.drag_overlay.draw_hover_overlay(self.screen)
        self.volume_overlay.draw_volume_bar(self.screen)
        self.title_overlay.draw_title_overlay(self.screen)

    def update_fft_data(self):
        if Settings.is_playing and pygame.mixer.music.get_busy():
            if not self.fft_worker_running:
                self.fft_worker_running = True
                thread = threading.Thread(target=self.fft_worker, daemon=True)
                thread.start()

    def fft_worker(self):
        try:
            current_sample_index = self.audio_processor.get_current_sample_index()

            if self.stop_fft_thread.is_set() or current_sample_index >= self.audio_length_samples:
                return

            sample_rate = self.audio_processor.get_sample_rate()
            self.title_overlay.update_time(current_sample_index, sample_rate)

            self.compute_and_store_fft(current_sample_index)
            
        except Exception as e:
            print(f"FFT worker error: {e}")
        finally:
            self.fft_worker_running = False

    def compute_and_store_fft(self, start_sample: int):
        freqs_mags = self.audio_processor.calculate_fft(
            start_sample=start_sample,
            num_samples=Settings.fft_window_size)

        if freqs_mags is not None:
            with self.fft_lock:
                self.freqs, self.mags = freqs_mags

    def load_and_play_sound(self, file: str):
        if self.audio_processor.load_audio_file(file):
            pygame.mixer.music.load(file)
            self.audio_length_samples = self.audio_processor.get_audio_length_samples()

            sample_rate = self.audio_processor.get_sample_rate()
            self.title_overlay.set_audio_info(file, self.audio_length_samples, sample_rate)

            with self.fft_lock:
                self.freqs = None
                self.mags = None
            self.music_play()

    def music_play(self):
        if not Settings.is_playing:
            Settings.is_playing = True
            pygame.mixer.music.play()
    
    def music_stop(self):
        if Settings.is_playing:
            Settings.is_playing = False
            pygame.mixer.music.stop()

    def music_unpause(self):
        if not Settings.is_playing:
            Settings.is_playing = True
            pygame.mixer.music.unpause()

    def music_pause(self):
        if Settings.is_playing:
            Settings.is_playing = False
            pygame.mixer.music.pause()

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_quit_event(event)
            self.handle_key_down_event(event)
            self.handle_drop_event(event)
            self.drag_overlay.handle_event(event)
            self.volume_overlay.handle_event(event)

    def handle_key_down_event(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.handle_space()

            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.handle_paste()

    def handle_space(self):
        if Settings.is_playing:
            self.music_pause()
        else:
            self.music_unpause()

    def handle_paste(self):
        print("CTRL+V detected; clipboard:!", repr(pyperclip.paste()))
        video_url = pyperclip.paste().strip()
        if video_url:
            path = self.youtubeHandler.get_audio_from_youtube(video_url)
            if path:
                self.load_and_play_sound(path)

    def handle_drop_event(self, event: pygame.event):
        if event.type == pygame.DROPFILE:
            if Settings.is_playing:
                self.music_stop()

            if self.file_handler.handle_file(event.file):
                self.load_and_play_sound(event.file)

    def handle_quit_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            self.running = False