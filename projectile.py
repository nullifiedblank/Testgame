import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, image, speed, lifetime, damage=10):
        super().__init__()

        self.image_orig = image
        self.image = pygame.transform.rotate(self.image_orig, angle + 45)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.damage = damage
        self.owner = 'player' # Default owner

        self.pos = pygame.math.Vector2(pos)
        angle_rad = math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * speed

    def update(self, hittable_sprites, hittable_sprites_2=None):
        self.pos += self.velocity
        self.rect.center = self.pos

        # --- Collision Detection ---
        groups_to_check = [hittable_sprites]
        if hittable_sprites_2:
            groups_to_check.append(hittable_sprites_2)

        for group in groups_to_check:
            collided_sprites = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)
            for sprite in collided_sprites:
                # Prevent projectiles from hitting their owner
                if hasattr(sprite, 'owner') and sprite.owner == self.owner:
                    continue

                # Check for invulnerability
                if hasattr(sprite, 'is_invulnerable') and sprite.is_invulnerable:
                    continue

                if hasattr(sprite, 'health'):
                    sprite.health.take_damage(self.damage)
                    self.kill() # Destroy projectile on hit
                    return # Stop checking after the first hit

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
