import pygame
from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN) # Using a simple color for now
        self.rect = self.image.get_rect(topleft=(x, y))

class EarthWall(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((96, 64))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=center_pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2500 # 2.5 seconds

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
