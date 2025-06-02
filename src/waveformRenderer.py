import pygame
from pygame import Surface


class WaveformRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = {
            'grid': (80, 80, 80),
        }
        
    def draw_grid(self, surface: Surface):
        grid_spacing = 50
        for x in range(0, self.width, grid_spacing):
            pygame.draw.line(surface, self.colors['grid'], (x, 0), (x, self.height), 1)
        for y in range(0, self.height, grid_spacing):
            pygame.draw.line(surface, self.colors['grid'], (0, y), (self.width, y), 1)