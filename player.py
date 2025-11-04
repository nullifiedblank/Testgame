import pygame
import math
from settings import *
from weapon import HeldWeapon # Import the new HeldWeapon class

# A helper function to load images
def load_image(file_path):
    try:
        return pygame.image.load(file_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {file_path} - {e}")
        placeholder = pygame.Surface((40, 60)); placeholder.fill(RED); return placeholder

class Player:
    def __init__(self, x, y):
        # --- Visuals ---
        self.image_right = load_image('assets/player.png')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.held_weapon = None # This will hold the HeldWeapon sprite

        # --- Stats ---
        self.speed = 5; self.max_health = 200; self.health = self.max_health
        self.max_energy = 200; self.energy = self.max_energy
        self.energy_regen_rate = 5; self.energy_regen_interval = 2000
        self.last_regen_time = 0

        # --- Weapon & Attack ---
        self.current_weapon_data = None
        self.combo_counter = 0; self.last_attack_time = 0

        # --- Skills ---
        self.skills = {}; self.is_dashing = False; self.is_invulnerable = False

    def set_weapon(self, weapon_data):
        """Equips a new weapon and creates the visual sprite for it."""
        self.current_weapon_data = weapon_data
        self.held_weapon = HeldWeapon(self, self.current_weapon_data.held_image)

    def handle_input(self, keys, mouse_pos):
        if self.is_dashing: return

        # --- Movement ---
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y -= 1
        if keys[pygame.K_s]: move_vector.y += 1
        if keys[pygame.K_a]: move_vector.x -= 1
        if keys[pygame.K_d]: move_vector.x += 1
        if move_vector.length() > 0:
            move_vector.normalize_ip(); self.pos += move_vector * self.speed

        # --- Aiming and Flipping ---
        dx, dy = mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
        self.angle = math.degrees(math.atan2(-dy, dx))

        # Flip the player image based on mouse position
        if dx < 0:
            self.image = self.image_left
        else:
            self.image = self.image_right

        self.rect.center = self.pos

    def attack(self, attack_sprites_group, projectile_group, is_attacking):
        if not self.current_weapon_data or self.is_dashing: return

        weapon = self.current_weapon_data
        current_time = pygame.time.get_ticks()

        if weapon.attack_type == 'LASER':
            if is_attacking and self.energy > 0:
                if current_time - self.last_attack_time > weapon.attack_cooldown:
                    self.energy -= 2
                    attack_data = weapon.attack_prefabs[0]
                    laser = weapon.attack_sprite_class(player=self, **attack_data)
                    attack_sprites_group.add(laser)
                    self.last_attack_time = current_time
            return

        if not is_attacking: return
        if current_time - self.last_attack_time < weapon.attack_cooldown: return
        if current_time - self.last_attack_time > weapon.combo_reset_time:
            self.combo_counter = 0

        attack_data = weapon.attack_prefabs[self.combo_counter].copy()

        if weapon.attack_type == 'MELEE':
            attack_data.pop('image_path', None)
            sprite = weapon.attack_sprite_class(player=self, **attack_data)
            attack_sprites_group.add(sprite)
        elif weapon.attack_type == 'RANGED':
            attack_data.pop('image_path', None)
            projectile = weapon.attack_sprite_class(pos=self.pos, angle=self.angle, **attack_data)
            projectile_group.add(projectile)

        self.last_attack_time = current_time
        self.combo_counter = (self.combo_counter + 1) % len(weapon.attack_prefabs)

    def activate_skill(self, skill_name):
        if skill_name in self.skills: self.skills[skill_name].activate()

    def update(self):
        self.handle_energy_regen()
        self.update_skills()
        if self.held_weapon: self.held_weapon.update()

        # We no longer clamp the position to the screen, the camera will follow
        self.rect.center = self.pos

    def update_skills(self):
        for skill in self.skills.values(): skill.update()

    def handle_energy_regen(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regen_time > self.energy_regen_interval:
            self.last_regen_time = current_time
            self.energy = min(self.max_energy, self.energy + self.energy_regen_rate)
