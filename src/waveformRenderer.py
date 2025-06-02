import pygame
from pygame import Surface
import numpy as np


class WaveformRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = {
            'grid': (80, 80, 80),
            'waveform': (0, 200, 255)
        }
        
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
            magnitude = mags[i]
            height_ratio = magnitude / max_mag
            waveform_height = height_ratio * self.height * 0.9

            if waveform_height < 1 and magnitude > 0:
                 waveform_height = 1 # Every non-zero frequency magnitude draws at least a 1-pixel-high bar

            x = int(i * bar_width)
            y = int(self.height - waveform_height)

            color_progress = i / (num_bins - 1) if num_bins > 1 else 0.0

            green = int(255 * (1.0 - color_progress))
            red = int(255 * color_progress)
            color = (red, green, 0)

            pygame.draw.rect(
                surface,
                color,
                (x, y, int(bar_width), int(waveform_height))
            )