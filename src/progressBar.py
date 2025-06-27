import pygame

class ProgressBar:
    def __init__(self, x, y, width, height, border_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_width = border_width

        self.max_value = 1.0
        self.current_value = 0.0

        self.outer_rect = pygame.Rect(x, y, width, height)
        self.inner_rect = pygame.Rect(
            x + border_width,
            y + border_width,
            width - (border_width * 2),
            height - (border_width * 2)
        )

        self.colors = {
            'border':       (60, 120, 255),
            'progress_bg':  (50, 50, 50),
            'progress':     (255, 255, 255),
        }

    def set_max_value(self, value: float):
        if value <= 0:
            return
        self.max_value = value

    def set_current_value(self, value: float):
        self.current_value = max(0.0, min(value, self.max_value))

    def draw_progress_bar(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.colors['border'], self.outer_rect)
        pygame.draw.rect(screen, self.colors['progress_bg'], self.inner_rect)

        if self.current_value > 0 and self.max_value > 0:
            progress_ratio = self.current_value / self.max_value
            progress_width = int(self.inner_rect.width * progress_ratio)

            if progress_width > 0:
                progress_fill_rect = pygame.Rect(
                    self.inner_rect.x,
                    self.inner_rect.y,
                    progress_width,
                    self.inner_rect.height
                )
                pygame.draw.rect(screen, self.colors['progress'], progress_fill_rect)