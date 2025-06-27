import pygame
import os
from settings import Settings
from progressBar import ProgressBar

class TitleOverlay:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.font_title = pygame.font.Font(None, 32)
        self.font_time = pygame.font.Font(None, 24)
        
        self.colors = {
            'text':         (255, 255, 255),
            'status_play':  (100, 255, 100),
            'status_pause': (255, 255, 100)
        }
        
        self.padding = 10
        progress_bar_y = 70
        progress_bar_height = 15
        progress_bar_border = 2

        self.progress_bar = ProgressBar(
            x=self.padding,
            y=progress_bar_y,
            width=self.width - (self.padding * 2),
            height=progress_bar_height,
            border_width=progress_bar_border
        )
        self.time_text_y = progress_bar_y - 25

        self.current_title = "No audio loaded"
        self.current_time = 0.0
        self.total_time = 0.0

    def set_audio_info(self, file_path: str, total_duration_samples: int, sample_rate: int):
        if file_path:
            filename = os.path.basename(file_path)
            self.current_title = os.path.splitext(filename)[0]
        else:
            self.current_title = "No audio loaded"

        self.total_time = total_duration_samples / sample_rate if sample_rate > 0 else 0.0
        self.current_time = 0.0

        self.progress_bar.set_max_value(self.total_time)
        self.progress_bar.set_current_value(0.0)

    def update_time(self, current_sample: int, sample_rate: int) -> None:
        if sample_rate > 0:
            self.current_time = current_sample / sample_rate
        else:
            self.current_time = 0.0
        self.progress_bar.set_current_value(self.current_time)

    def format_time(self, seconds: float) -> str:
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def draw_title_overlay(self, screen: pygame.Surface):
        if Settings.is_dragging_over or screen is None:
            return
        
        self.draw_title(screen)
        self.draw_status(screen)
        self.progress_bar.draw_progress_bar(screen)
        self.draw_time(screen)
        
    def draw_title(self, screen: pygame.Surface):
        title_surface = self.font_title.render(self.current_title, True, self.colors['text'])
        screen.blit(title_surface, (self.padding, self.padding))

    def draw_status(self, screen: pygame.Surface):
        status_text = "Playing" if Settings.is_playing else "Paused"
        status_color = self.colors['status_play'] if Settings.is_playing else self.colors['status_pause']
        status_surface = self.font_time.render(f"[{status_text}]", True, status_color)
        
        title_width = self.font_title.size(self.current_title)[0]
        screen.blit(status_surface, (self.padding + title_width + 15, self.padding + 5))

    def draw_time(self, screen: pygame.Surface):
        current_time_str = self.format_time(self.current_time)
        total_time_str = self.format_time(self.total_time)
        time_text = f"{current_time_str} / {total_time_str}"

        time_surface = self.font_time.render(time_text, True, self.colors['text'])
        screen.blit(time_surface, (self.padding, self.time_text_y))