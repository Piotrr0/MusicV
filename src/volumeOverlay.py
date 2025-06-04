import pygame
from settings import Settings

class VolumeOverlay():
    def __init__(self, screen_width):
        self.volume_percent = 100
        self.font = pygame.font.Font(None, 24)

        self.slider_width = 150
        self.slider_height = 10
        self.slider_knob_radius = 8
        self.border_padding = 6

        self.slider_x = screen_width - self.slider_width - 10
        self.slider_y = 10

        self.slider_rect = pygame.Rect(
            self.slider_x - self.border_padding,
            self.slider_y - self.border_padding,
            self.slider_width + self.border_padding * 2,
            self.slider_height + self.border_padding * 2
        )

        self.colors = {
            'slider':   (255, 255, 255),
            'knob':     (255, 255, 255),
            'bg':       (50, 50, 50),
            'border':   (60, 120, 255)
        }

    def draw_volume_bar(self, screen: pygame.Surface):
        if Settings.is_dragging_over:
            return

        pygame.draw.rect(screen, self.colors['border'], self.slider_rect, 10)
        pygame.draw.rect(screen, self.colors['bg'], (self.slider_x, self.slider_y, self.slider_width, self.slider_height))

        knob_x = self.slider_x + int((1 - self.volume_percent / 100) * self.slider_width)
        pygame.draw.circle(screen, self.colors['knob'], (knob_x, self.slider_y + self.slider_height // 2), self.slider_knob_radius)

        self.draw_text(screen)

    def draw_text(self, screen: pygame.Surface):
        text = f"Volume: {self.volume_percent}%"
        surface = self.font.render(text, True, self.colors['slider'])
        screen.blit(surface, (self.slider_x + 45, self.slider_y + self.slider_height + 10))

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

    def detect_volume_dragging(self, pos: tuple):
        knob_center_x = self.slider_x + int((1 - self.volume_percent / 100) * self.slider_width)
        knob_center_y = self.slider_y + self.slider_height // 2

        knob_rect = pygame.Rect(
            knob_center_x - self.slider_knob_radius,
            knob_center_y - self.slider_knob_radius,
            self.slider_knob_radius * 2,
            self.slider_knob_radius * 2
        )

        if knob_rect.collidepoint(pos):
            Settings.is_dragging_volume = True

    def handle_volume_dragging(self, pos: tuple):
        new_knob_x = max(self.slider_x, min(self.slider_x + self.slider_width, pos[0]))
        self.volume_percent = int((1 - (new_knob_x - self.slider_x) / self.slider_width) * 100)
        pygame.mixer.music.set_volume(self.volume_percent / 100)
