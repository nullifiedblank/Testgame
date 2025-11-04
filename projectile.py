import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed, lifetime, size=(10, 20), color=WHITE):
        super().__init__()

        # The visual representation of the projectile
        self.image_orig = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image_orig, color, (0, 0, *size))
        self.image = pygame.transform.rotate(self.image_orig, angle)

        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

        # Store the precise position and velocity
        self.pos = pygame.math.Vector2(pos)
        angle_rad = pygame.math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(pygame.math.cos(angle_rad), -pygame.math.sin(angle_rad)) * speed

    def update(self):
        # Move the projectile based on its velocity
        self.pos += self.velocity
        self.rect.center = self.pos

        # Remove the projectile after its lifetime expires
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
