import pygame
from pygame import Surface
import numpy as np


class WaveformRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = {
            'grid': (80, 80, 80), }
        self.waveform_scale = 0.85
        
    def draw_grid(self, surface: Surface):
        grid_spacing = 50
        for x in range(0, self.width, grid_spacing):
            pygame.draw.line(surface, self.colors['grid'], (x, 0), (x, self.height), 1)
        for y in range(0, self.height, grid_spacing):
            pygame.draw.line(surface, self.colors['grid'], (0, y), (self.width, y), 1)

    def draw_waveform_fft(self, surface: Surface, freqs: np.ndarray, mags: np.ndarray):
        if mags is None or len(mags) == 0:
            return

        num_bins = len(mags)
        if num_bins == 0:
            return

        bar_width = max(1, self.width / num_bins)

        max_mag = np.max(mags)
        if max_mag == 0:
            max_mag = 1e-6

        for i in range(num_bins):
            waveform_height = self.calculate_waveform_height(mags[i], max_mag)

            x = int(i * bar_width)
            y = int(self.height - waveform_height)
            
            pygame.draw.rect(
                surface,
                self.get_color(i,num_bins),
                (x, y, int(bar_width), int(waveform_height))
            )

    def calculate_waveform_height(self, magnitude: float, max_magnitude: float) -> float:
        height_ratio = magnitude / max_magnitude
        waveform_height = height_ratio * self.height * self.waveform_scale

        if waveform_height < 1 and magnitude > 0:
                 waveform_height = 1 # Every non-zero frequency magnitude draws at least a 1-pixel-high bar
                 
        return waveform_height
        
    def get_color(self, current_bin: int, num_bins: int) -> tuple:
            color_progress = current_bin / (num_bins - 1) if num_bins > 1 else 0.0

            green = int(255 * (1.0 - color_progress))
            red = int(255 * color_progress)
            return (red, green, 0)
    
    def get_max_waveform_height(self) -> float:
         return self.height * self.waveform_scale
