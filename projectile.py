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
        self.team_id = 0
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
                # --- Team System ---
                if hasattr(sprite, 'team_id') and sprite.team_id == self.team_id:
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
        self.damage = 30
        self.owner = owner
        self.team_id = owner.team_id
        self.bounce_count = 0
        self.friction = 0.995 # Slight velocity decay

    def update(self, hittable_sprites, player_group, wall_sprites):
        self.velocity *= self.friction
        self.pos += self.velocity
        self.rect.center = self.pos

        # --- End Conditions ---
        if self.velocity.magnitude() < 60:
            self.kill()
            return

        # --- Wall & Enemy Collision ---
        collided_walls = pygame.sprite.spritecollide(self, wall_sprites, False)
        enemies_hit = pygame.sprite.spritecollide(self, hittable_sprites, False)

        valid_enemies_hit = []
        for enemy in enemies_hit:
            if hasattr(enemy, 'team_id') and enemy.team_id != self.team_id:
                valid_enemies_hit.append(enemy)

        all_collided_obstacles = collided_walls + valid_enemies_hit

        if all_collided_obstacles:
            # --- Damage Logic (Non-Piercing) ---
            if valid_enemies_hit:
                first_enemy = valid_enemies_hit[0]
                if hasattr(first_enemy, 'health'):
                    first_enemy.health.take_damage(self.damage)
                    if self.owner and hasattr(self.owner, 'talisman') and self.owner.talisman:
                        self.owner.talisman.on_deal_damage(self.owner, first_enemy)

            # --- Bounce Logic ---
            self.bounce_count += 1
            if self.bounce_count >= 4:
                self.kill()
                return

            self.pos -= self.velocity # Move back to pre-collision position

            temp_obstacle_group = pygame.sprite.Group(all_collided_obstacles)

            # Check for collision on each axis separately
            self.rect.centerx = self.pos.x + self.velocity.x
            if pygame.sprite.spritecollide(self, temp_obstacle_group, False):
                self.velocity.x *= -1
            self.rect.centery = self.pos.y + self.velocity.y
            if pygame.sprite.spritecollide(self, temp_obstacle_group, False):
                self.velocity.y *= -1

            self.damage *= 0.75
