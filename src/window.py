import pygame
from waveformRenderer import WaveformRenderer

class Window():
    def __init__(self):
        self.background_color = (15, 15, 25)
        self.width, self.height = (1200, 800)
    
        pygame.init()
        pygame.display.set_caption("Audio Waveform Visualizer")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True

        self.renderer = WaveformRenderer(self.width, self.height)

    def update(self):
        while self.running:
            self.handle_events()
            self.screen.fill(self.background_color)

            self.renderer.draw_grid(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False