import pygame
from waveformRenderer import WaveformRenderer
from dragOverlay import DragOverlay

class Window():
    def __init__(self):
        self.width, self.height = (1200, 800)
        self.colors = {
            'bg': (128, 128, 128),
        }

        self.is_dragging_over = False
    
        pygame.init()
        pygame.display.set_caption("Audio Waveform Visualizer")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True

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