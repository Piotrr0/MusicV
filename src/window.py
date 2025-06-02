import pygame
from pygame import event
from waveformRenderer import WaveformRenderer

class Window():
    def __init__(self):
        self.width, self.height = (1200, 800)
        self.colors = {
            'bg': (128, 128, 128),
            'bg_hover': (100, 100, 110),
            'overlay': (0, 0, 0, 128),
            'border_drag': (60, 120, 255),
            'text_drag': (255, 255, 255)
        }

        self.is_dragging_over = False
    
        pygame.init()
        pygame.display.set_caption("Audio Waveform Visualizer")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True

        self.renderer = WaveformRenderer(self.width, self.height)

        self.drop_text_surface = self.font.render("Drop Audio File Here", True, self.colors['text_drag'])
        self.drop_text_rect = self.drop_text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.overlay_border_size = 10

    def get_background_color(self) -> tuple:
        if self.is_dragging_over:
            return self.colors['bg_hover']
        else: 
            return self.colors['bg']

    def update(self):
        while self.running:
            self.handle_events()

            self.screen.fill(self.get_background_color())

            self.renderer.draw_grid(self.screen)
            self.draw_hovering_overlay()


            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_hovering_overlay(self):
        if self.is_dragging_over:
            overlay_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay_surface.fill(self.colors['overlay'])
            self.screen.blit(overlay_surface, (0, 0))

            pygame.draw.rect(self.screen, self.colors['border_drag'], self.screen.get_rect(), self.overlay_border_size)

            self.screen.blit(self.drop_text_surface, self.drop_text_rect)        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            self.handle_drop_events(event)

    def handle_drop_events(self, event):
        if event.type == pygame.DROPBEGIN:
            self.is_dragging_over = True

        elif event.type == pygame.DROPCOMPLETE:
            self.is_dragging_over = False

        elif event.type == pygame.DROPFILE:
            file_path = event.file
            self.is_dragging_over = False