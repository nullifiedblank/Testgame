import pygame
import math
from settings import *

class Player:
    def __init__(self, x, y):
        # ... (init code is unchanged) ...
        self.image_orig = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image_orig, RED, [(0, 40), (20, 0), (40, 40)])
        self.image = self.image_orig
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.speed = 5
        self.max_health = 200
        self.health = self.max_health
        self.max_energy = 200
        self.energy = self.max_energy
        self.energy_regen_rate = 5
        self.energy_regen_interval = 2000
        self.last_regen_time = 0
        self.current_weapon = None
        self.combo_counter = 0
        self.last_attack_time = 0
        self.skills = {}
        self.is_dashing = False
        self.is_invulnerable = False

    def handle_input(self, keys, mouse_pos):
        # ... (unchanged) ...
        if self.is_dashing: return
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y -= 1
        if keys[pygame.K_s]: move_vector.y += 1
        if keys[pygame.K_a]: move_vector.x -= 1
        if keys[pygame.K_d]: move_vector.x += 1
        if move_vector.length() > 0:
            move_vector.normalize_ip()
            self.pos += move_vector * self.speed
        dx, dy = mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def attack(self, attack_sprites_group, projectile_group, is_attacking):
        if not self.current_weapon or self.is_dashing: return

        current_time = pygame.time.get_ticks()

        if self.current_weapon.attack_type == 'LASER':
            if is_attacking and self.energy > 0:
                if current_time - self.last_attack_time > self.current_weapon.attack_cooldown:
                    self.energy -= 2
                    attack_data = self.current_weapon.attack_prefabs[0]
                    laser_sprite = self.current_weapon.attack_sprite_class(player=self, **attack_data)
                    attack_sprites_group.add(laser_sprite)
                    self.last_attack_time = current_time
            return

        if not is_attacking: return

        if current_time - self.last_attack_time < self.current_weapon.attack_cooldown: return

        if current_time - self.last_attack_time > self.current_weapon.combo_reset_time:
            self.combo_counter = 0

        attack_data = self.current_weapon.attack_prefabs[self.combo_counter]

        if self.current_weapon.attack_type == 'MELEE':
            angle_rad = math.radians(self.angle + 90)
            spawn_pos = self.pos + pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * 60
            attack_sprite = self.current_weapon.attack_sprite_class(player=self, pos=spawn_pos, rotation=self.angle, **attack_data)
            attack_sprites_group.add(attack_sprite)

        elif self.current_weapon.attack_type == 'RANGED':
            projectile = self.current_weapon.attack_sprite_class(pos=self.pos, angle=self.angle, **attack_data)
            projectile_group.add(projectile)

        self.last_attack_time = current_time
        self.combo_counter = (self.combo_counter + 1) % len(self.current_weapon.attack_prefabs)

    def activate_skill(self, skill_name):
        if skill_name in self.skills:
            self.skills[skill_name].activate()

    def update(self):
        self.handle_energy_regen()
        self.update_skills()

    def update_skills(self):
        for skill in self.skills.values():
            skill.update()

    def handle_energy_regen(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regen_time > self.energy_regen_interval:
            self.last_regen_time = current_time
            self.energy = min(self.max_energy, self.energy + self.energy_regen_rate)
