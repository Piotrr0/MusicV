import pygame
from settings import Settings

class VolumeOverlay():
    def __init__(self):
        self.volume_percent = 100
        self.font = pygame.font.Font(None, 24)

        self.slider_x = 10
        self.slider_y = 40
        self.slider_width = 150
        self.slider_height = 10
        self.slider_knob_radius = 8

        self.colors = {
            'slider': (255, 255, 255),
            'knob': (255, 255, 255),
            'bg': (50,50,50)
        }

    def draw_volume_bar(self, screen):
        if Settings.is_dragging_over:
            return None

        pygame.draw.rect(screen, self.colors['bg'], (self.slider_x, self.slider_y, self.slider_width, self.slider_height))

        knob_x = self.slider_x + int((self.volume_percent / 100) * self.slider_width)
        pygame.draw.circle(screen, self.colors['knob'], (knob_x, self.slider_y + self.slider_height // 2), self.slider_knob_radius)

        text = f"Volume: {self.volume_percent}%"
        surface = self.font.render(text, True, self.colors['slider'])
        screen.blit(surface, (self.slider_x, self.slider_y - 25))

    def handle_event(self, event: pygame.event.EventType):
        if event.type == pygame.MOUSEWHEEL:
            self.volume_percent = max(0, min(100, self.volume_percent + event.y))
            pygame.mixer.music.set_volume(self.volume_percent / 100)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.detect_volume_dragging(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            if Settings.is_dragging_volume:
                self.handle_volume_dragging(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                Settings.is_dragging_volume = False

    
    def detect_volume_dragging(self, pos:tuple):
        knob_center_x = self.slider_x + int((self.volume_percent / 100) * self.slider_width)
        knob_center_y = self.slider_y + self.slider_height // 2
                
        if pygame.Rect(knob_center_x - self.slider_knob_radius, 
                        knob_center_y - self.slider_knob_radius, 
                        self.slider_knob_radius * 2, 
                        self.slider_knob_radius * 2).collidepoint(pos):
            Settings.is_dragging_volume = True

    def handle_volume_dragging(self, pos: tuple):
        new_knob_x = max(self.slider_x, min(self.slider_x + self.slider_width, pos[0]))
        self.volume_percent = int(((new_knob_x - self.slider_x) / self.slider_width) * 100)
        pygame.mixer.music.set_volume(self.volume_percent / 100)