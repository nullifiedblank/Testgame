import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, image, speed, lifetime):
        super().__init__()

        self.image_orig = image
        self.image = pygame.transform.rotate(self.image_orig, angle)

        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

        self.pos = pygame.math.Vector2(pos)
        angle_rad = math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * speed

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
