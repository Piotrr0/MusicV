import pygame
from waveformRenderer import WaveformRenderer
from dragOverlay import DragOverlay
from dropFileHandler import DropFileHandler
from audioProcessor import AudioProcessor

class Window():
    def __init__(self):
        self.width, self.height = (1200, 800)
        self.colors = {
            'bg': (128, 128, 128),
        }

        self.is_dragging_over = False
    
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

    def update(self):
        while self.running:
            self.handle_events()

            self.screen.fill(self.drag_overlay.get_background_color(self.colors['bg']))

            self.wave_renderer.draw_grid(self.screen)
            self.drag_overlay.draw_hover_overlay(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.drag_overlay.handle_event(event)
    
            if event.type == pygame.DROPFILE:
                if self.file_handler.handle_file(event.file):
                    data = self.audio_processor.load_audio_file(event.file)
                    print(data)

                freqs_mags = self.audio_processor.get_fft_data(
                start_sample=0,
                fft_size=1024,
                channel_index=0)

                if freqs_mags is not None:
                    freqs, mags = freqs_mags
                    print("Freqs array:", freqs)
                    print("Mags array:", mags)