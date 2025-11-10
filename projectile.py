import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, image, speed, lifetime, damage=10, has_slow=False):
        super().__init__()

        self.image_orig = image
        self.image = pygame.transform.rotate(self.image_orig, angle + 45)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.damage = damage
        self.owner = 'player' # Default owner
        self.has_slow = has_slow

        self.pos = pygame.math.Vector2(pos)
        angle_rad = math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * speed

    def update(self, hittable_sprites, hittable_sprites_2=None, wall_sprites=None):
        self.pos += self.velocity
        self.rect.center = self.pos

        # --- Wall Collision ---
        if wall_sprites and pygame.sprite.spritecollide(self, wall_sprites, False):
            self.kill()
            return

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

                    # --- Talisman Integration ---
                    if self.owner and hasattr(self.owner, 'talisman') and self.owner.talisman:
                        self.owner.talisman.on_deal_damage(self.owner, sprite, self.has_slow)

                    self.kill() # Destroy projectile on hit
                    return # Stop checking after the first hit

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

class ReboundBall(pygame.sprite.Sprite):
    def __init__(self, pos, angle, image, speed, damage, owner):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        angle_rad = math.radians(angle + 90)
        self.velocity = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * speed
        self.damage = damage
        self.owner = owner
        self.bounce_count = 0
        self.friction = 0.995 # Slight velocity decay

    def update(self, hittable_sprites, wall_sprites):
        self.velocity *= self.friction
        self.pos += self.velocity
        self.rect.center = self.pos

        # --- End Conditions ---
        if self.velocity.magnitude() < 60:
            self.kill()
            return

        # --- Wall Collision ---
        collided_walls = pygame.sprite.spritecollide(self, wall_sprites, False)
        if collided_walls:
            self.bounce_count += 1
            if self.bounce_count >= 4:
                self.kill()
                return

            # --- Better Reflection Logic ---
            # Move the ball back to its position before the collision
            self.pos -= self.velocity
            self.rect.center = self.pos

            # Check for horizontal or vertical collision
            # This is a simplified approach, a more robust solution would use vector projection
            # But for simple horizontal/vertical walls, this works.
            if self.rect.left < collided_walls[0].rect.right and self.rect.right > collided_walls[0].rect.left:
                self.velocity.y *= -1 # Vertical collision
            else:
                self.velocity.x *= -1 # Horizontal collision

            self.damage *= 0.75

        # --- Enemy Collision ---
        collided_enemies = pygame.sprite.spritecollide(self, hittable_sprites, False)
        for enemy in collided_enemies:
            if hasattr(enemy, 'health'):
                enemy.health.take_damage(self.damage)
                if self.owner and hasattr(self.owner, 'talisman') and self.owner.talisman:
                    self.owner.talisman.on_deal_damage(self.owner, enemy)
