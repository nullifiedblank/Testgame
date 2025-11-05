import pygame
import math
from settings import *
from health import Health

class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, player, asset_manager):
        super().__init__()
        self.player = player
        self.asset_manager = asset_manager
        self.image_orig = self.asset_manager.get('assets/enemies/turret.png')
        self.image = self.image_orig
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0

        self.health = Health(self, 50)

        self.fire_rate = 2000
        self.last_shot_time = 0

    def update(self, projectile_group):
        self.aim_at_player()
        self.shoot(projectile_group)

    def aim_at_player(self):
        dx, dy = self.player.pos.x - self.pos.x, self.player.pos.y - self.pos.y
        self.angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def shoot(self, projectile_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.fire_rate:
            self.last_shot_time = current_time

            from projectile import Projectile

            attack_data = {
                "image": self.asset_manager.get('assets/projectiles/enemy_bullet.png'),
                "speed": 10,
                "lifetime": 5000,
                "damage": 5
            }

            projectile = Projectile(pos=self.pos, angle=self.angle, **attack_data)
            projectile.owner = 'enemy'
            projectile_group.add(projectile)
