import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed, lifetime):
        super().__init__()

        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, WHITE, (0, 0, 10, 20))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

        # Calculate velocity based on player's angle
        angle_rad = pygame.math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(pygame.math.cos(angle_rad), -pygame.math.sin(angle_rad)) * speed
        self.pos = pygame.math.Vector2(pos)

    def update(self):
        # Move the projectile
        self.pos += self.velocity
        self.rect.center = self.pos

        # Check for lifetime expiration
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

        # Check if it goes off-screen (another form of cleanup)
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
             pass # For now, we'll let lifetime handle it. Later, this could be terrain collision.
