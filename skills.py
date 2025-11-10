import pygame
import math

class AfterImage(pygame.sprite.Sprite):
    def __init__(self, x, y, image, lifetime=200):
        super().__init__()
        self.image = image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.alpha = 128
        self.image.set_alpha(self.alpha)

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        if elapsed > self.lifetime:
            self.kill()
            return

        self.alpha = 128 * (1 - (elapsed / self.lifetime))
        self.image.set_alpha(self.alpha)

class Skill:
    def __init__(self, player, cooldown, energy_cost):
        self.player = player
        self.cooldown = cooldown
        self.energy_cost = energy_cost
        self.last_used_time = -cooldown

    def can_use(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_used_time > self.cooldown and
                self.player.energy >= self.energy_cost)

    def activate(self):
        if self.can_use():
            self.player.energy -= self.energy_cost
            self.last_used_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        pass

class DashSkill(Skill):
    def __init__(self, player, all_sprites_group):
        super().__init__(player, cooldown=4000, energy_cost=15)
        self.dash_speed = 30
        self.dash_duration = 100 # ms
        self.dash_start_time = 0
        self.after_image_group = all_sprites_group
        self.after_image_timer = 0
        self.after_image_interval = 30 # ms

    def activate(self):
        if super().activate():
            self.player.is_dashing = True
            self.player.is_invulnerable = True
            self.dash_start_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.player.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time <= self.dash_duration:
                angle_rad = math.radians(self.player.angle + 90)
                move_vector = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
                self.player.pos += move_vector * self.dash_speed
                self.player.rect.center = self.player.pos

                if current_time - self.after_image_timer > self.after_image_interval:
                    self.after_image_timer = current_time
                    after_image = AfterImage(self.player.pos.x, self.player.pos.y, self.player.image)
                    self.after_image_group.add(after_image)
            else:
                self.player.is_dashing = False
                self.player.is_invulnerable = False
