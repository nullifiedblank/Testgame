import pygame
import math
from settings import *
from projectile import Projectile

# A helper function to load images
def load_image(file_path):
    try:
        return pygame.image.load(file_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {file_path} - {e}")
        placeholder = pygame.Surface((30, 30))
        placeholder.fill(RED)
        return placeholder

# --- Weapon Sprite (the one the player holds) ---
class HeldWeapon(pygame.sprite.Sprite):
    def __init__(self, player, image):
        super().__init__()
        self.player = player
        self.image_orig = image
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        # The weapon's image rotates to follow the player's aiming angle
        self.image = pygame.transform.rotate(self.image_orig, self.player.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

# --- Attack Visuals ---
class AttackSprite(pygame.sprite.Sprite):
    # ... (code is unchanged)
    def __init__(self, player, image, lifetime):
        super().__init__()
        self.player = player
        self.image_orig = image
        self.image = pygame.transform.rotate(self.image_orig, player.angle)
        self.rect = self.image.get_rect()
        self.offset = pygame.math.Vector2(80, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.update()
    def update(self):
        rotated_offset = self.offset.rotate(-self.player.angle)
        new_pos = self.player.pos + rotated_offset
        self.rect.center = new_pos
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

class Laser(pygame.sprite.Sprite):
    # ... (code is unchanged) ...
    def __init__(self, player, lifetime):
        super().__init__()
        self.player = player
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.image_orig = pygame.Surface((5, 1000), pygame.SRCALPHA)
        pygame.draw.rect(self.image_orig, RED, (0, 0, 5, 1000))
        self.image = self.image_orig
        self.rect = self.image.get_rect(midbottom=player.rect.center)
    def update(self):
        self.image = pygame.transform.rotate(self.image_orig, self.player.angle)
        angle_rad = math.radians(self.player.angle + 90)
        offset = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * 500
        self.rect = self.image.get_rect(center=self.player.pos + offset)
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

# --- Weapon Data Structure ---
class WeaponData:
    def __init__(self, held_image_path, attack_type, attack_cooldown, combo_reset_time, attack_prefabs, attack_sprite_class=AttackSprite):
        self.held_image = load_image(held_image_path)
        self.attack_type = attack_type
        self.attack_cooldown = attack_cooldown
        self.combo_reset_time = combo_reset_time
        self.attack_prefabs = [{'image': load_image(p['image_path']), **p} if 'image_path' in p else p for p in attack_prefabs]
        self.attack_sprite_class = attack_sprite_class

# --- ======================= WEAPON DEFINITIONS ======================= ---
sword_weapon = WeaponData(
    held_image_path="assets/sword.png", attack_type='MELEE', attack_cooldown=300, combo_reset_time=800,
    attack_prefabs=[{"image_path": "assets/sword_slash.png", "lifetime": 150}] * 2 + [{"image_path": "assets/sword_thrust.png", "lifetime": 250}]
)
spear_weapon = WeaponData(
    held_image_path="assets/spear.png", attack_type='MELEE', attack_cooldown=250, combo_reset_time=600,
    attack_prefabs=[{"image_path": "assets/spear_thrust.png", "lifetime": 200}] * 2 + [{"image_path": "assets/spear_barrage.png", "lifetime": 100}]
)
bow_weapon = WeaponData(
    held_image_path="assets/bow.png", attack_type='RANGED', attack_cooldown=800, combo_reset_time=1000,
    attack_prefabs=[{"image_path": "assets/arrow.png", "speed": 25, "lifetime": 10000}],
    attack_sprite_class=Projectile
)
wand_weapon = WeaponData(
    held_image_path="assets/wand.png", attack_type='RANGED', attack_cooldown=400, combo_reset_time=900,
    attack_prefabs=[{"image_path": "assets/small_orb.png", "speed": 15, "lifetime": 3000}] * 2 + [{"image_path": "assets/big_orb.png", "speed": 7, "lifetime": 4000}],
    attack_sprite_class=Projectile
)
staff_weapon = WeaponData(
    held_image_path="assets/staff.png", attack_type='LASER', attack_cooldown=100, combo_reset_time=0,
    attack_prefabs=[{"lifetime": 100}], attack_sprite_class=Laser
)

WEAPONS = {
    "sword": sword_weapon, "spear": spear_weapon, "bow": bow_weapon,
    "wand": wand_weapon, "staff": staff_weapon
}
