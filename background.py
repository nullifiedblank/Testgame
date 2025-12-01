import pygame
from settings import *

def create_checkerboard(width, height, tile_size):
    """Creates a large checkerboard surface to serve as the game background."""
    background = pygame.Surface((width, height))
    dark_grey = (40, 40, 40)
    light_grey = (50, 50, 50)

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            # Determine the color by the tile's position
            if (x // tile_size) % 2 == (y // tile_size) % 2:
                color = dark_grey
            else:
                color = light_grey
            pygame.draw.rect(background, color, rect)

    return background
