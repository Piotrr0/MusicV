import pygame

class DragOverlay:
    def __init__(self, parent_width: int, parent_height: int):
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.font = pygame.font.Font(None, 24)

        self.colors = {
            'bg_hover':       (100, 100, 110),
            'overlay':        (0, 0, 0, 128),
            'border_drag':    (60, 120, 255),
            'text_drag':      (255, 255, 255)
        }

        self.drop_text_surface = self.font.render("Drop Audio File Here", True, self.colors['text_drag'])
        self.drop_text_rect = self.drop_text_surface.get_rect(
            center=(self.parent_width // 2, self.parent_height // 2)
        )

        self.overlay_border_size = 10
        self.is_dragging_over = False

    def get_background_color(self, normal_bg: tuple) -> tuple:
        if self.is_dragging_over:
            return self.colors['bg_hover']
        return normal_bg
    
    def handle_event(self, event: pygame.event.EventType):
        if event.type == pygame.DROPBEGIN:
            self.is_dragging_over = True

        elif event.type == pygame.DROPCOMPLETE:
            self.is_dragging_over = False

        elif event.type == pygame.DROPFILE:
            self.is_dragging_over = False

    def draw_hover_overlay(self, screen: pygame.Surface):
        if not self.is_dragging_over:
            return

        overlay_surface = pygame.Surface((self.parent_width, self.parent_height), pygame.SRCALPHA)
        overlay_surface.fill(self.colors['overlay'])
        screen.blit(overlay_surface, (0, 0))

        pygame.draw.rect(screen, self.colors['border_drag'], screen.get_rect(), self.overlay_border_size)
        screen.blit(self.drop_text_surface, self.drop_text_rect)