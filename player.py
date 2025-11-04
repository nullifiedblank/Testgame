import pygame
import math
from settings import *
from weapon import HeldWeapon, WeaponAnimation

class Player:
    def __init__(self, x, y, asset_manager):
        self.asset_manager = asset_manager

        # --- Visuals ---
        self.image_right = self.asset_manager.get('player')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.held_weapon = None

        # --- Stats ---
        self.speed = 5; self.max_health = 200; self.health = self.max_health
        self.max_energy = 200; self.energy = self.max_energy
        self.energy_regen_rate = 5; self.energy_regen_interval = 2000
        self.last_regen_time = 0

        # --- Weapon & Attack ---
        self.weapon = None; self.combo_counter = 0; self.last_attack_time = 0
        self.active_animation = None; self.bow_anim_timer = 0; self.bow_anim_stage = 0

        # --- Skills ---
        self.skills = {}
        self.is_dashing = False
        self.is_invulnerable = False

    def set_weapon(self, weapon_data, sprite_group):
        self.weapon = weapon_data
        if self.held_weapon: self.held_weapon.kill()
        self.held_weapon = HeldWeapon(self, self.asset_manager.get(self.weapon.held_image_path))
        sprite_group.add(self.held_weapon)

    def handle_input(self, keys, mouse_pos):
        if self.is_dashing: return
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y -= 1
        if keys[pygame.K_s]: move_vector.y += 1
        if keys[pygame.K_a]: move_vector.x -= 1
        if keys[pygame.K_d]: move_vector.x += 1
        if move_vector.length() > 0:
            move_vector.normalize_ip(); self.pos += move_vector * self.speed
        dx, dy = mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
        self.angle = math.degrees(math.atan2(-dy, dx))
        if dx < 0: self.image = self.image_left
        else: self.image = self.image_right
        self.rect.center = self.pos

    def attack(self, hittable_sprites, projectile_group, is_attacking):
        if not self.weapon or self.is_dashing or (self.active_animation and not self.active_animation.is_done): return
        current_time = pygame.time.get_ticks()

        # Ranged Charge (Bow)
        if 'bow_draw_image' in self.weapon.extra_assets_paths:
            if is_attacking and self.bow_anim_stage == 0 and current_time - self.last_attack_time > self.weapon.attack_cooldown:
                self.bow_anim_stage = 1
                self.bow_anim_timer = current_time
                self.held_weapon.image_orig = self.asset_manager.get(self.weapon.extra_assets_paths['bow_empty_image'])
                attack_data = self.weapon.attack_data[0].copy()
                attack_data['image'] = self.asset_manager.get(attack_data.pop('image_path'))
                projectile = self.weapon.attack_sprite_class(pos=self.pos, angle=self.angle, **attack_data)
                projectile_group.add(projectile)
                self.last_attack_time = current_time
            return

        # Laser
        if self.weapon.attack_type == 'LASER':
            if is_attacking and self.energy > 0:
                if current_time - self.last_attack_time > self.weapon.attack_cooldown:
                    self.energy -= 2
                    laser_sprite = self.weapon.attack_sprite_class(player=self, **self.weapon.attack_data[0])
                    hittable_sprites.add(laser_sprite)
                    self.last_attack_time = current_time
            return

        if not is_attacking: return
        if current_time - self.last_attack_time < self.weapon.attack_cooldown: return
        if current_time - self.last_attack_time > self.weapon.combo_reset_time:
            self.combo_counter = 0

        attack_data = self.weapon.attack_data[self.combo_counter].copy()

        if self.weapon.attack_type == 'MELEE':
            self.active_animation = WeaponAnimation(self.held_weapon, attack_data, hittable_sprites)

        elif self.weapon.attack_type == 'RANGED':
            attack_data['image'] = self.asset_manager.get(attack_data.pop('image_path'))
            projectile = self.weapon.attack_sprite_class(pos=self.pos, angle=self.angle, **attack_data)
            projectile_group.add(projectile)

        self.last_attack_time = current_time
        self.combo_counter = (self.combo_counter + 1) % len(self.weapon.attack_data)

    def activate_skill(self, skill_name):
        if skill_name in self.skills: self.skills[skill_name].activate()

    def update(self):
        self.handle_energy_regen()
        self.update_skills()
        self.handle_bow_animation()
        if self.active_animation:
            self.active_animation.update()
            if self.active_animation.is_done:
                self.active_animation = None
                self.held_weapon.set_anim_rotation(0); self.held_weapon.set_anim_offset(0)
        self.rect.center = self.pos

    def handle_bow_animation(self):
        if self.bow_anim_stage == 0: return
        current_time = pygame.time.get_ticks()
        if self.bow_anim_stage == 1 and current_time - self.bow_anim_timer > 150:
            self.held_weapon.image_orig = self.asset_manager.get(self.weapon.extra_assets_paths['bow_draw_image'])
            self.bow_anim_stage = 2
        elif self.bow_anim_stage == 2 and current_time - self.bow_anim_timer > 400:
            self.held_weapon.image_orig = self.asset_manager.get(self.weapon.held_image_path)
            self.bow_anim_stage = 0

    def update_skills(self):
        for skill in self.skills.values(): skill.update()

    def handle_energy_regen(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regen_time > self.energy_regen_interval:
            self.last_regen_time = current_time
            self.energy = min(self.max_energy, self.energy + self.energy_regen_rate)
