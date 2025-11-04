import pygame
import math
from settings import *
from projectile import Projectile

# --- Attack Visuals ---
class AttackSprite(pygame.sprite.Sprite):
    def __init__(self, player, pos, rotation, size, color, lifetime):
        super().__init__()
        self.player = player
        self.offset = pos - player.pos # Calculate initial offset from player
        self.rotation = rotation

        self.image_orig = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image_orig, color, (0, 0, *size))
        self.image = pygame.transform.rotate(self.image_orig, rotation)
        self.rect = self.image.get_rect(center=pos)

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

    def update(self):
        # Update position to stay in front of the player, maintaining initial offset
        self.image = pygame.transform.rotate(self.image_orig, self.player.angle)

        angle_rad = math.radians(self.player.angle + 90)
        rotated_offset = self.offset.rotate(-self.player.angle) # Rotate the original offset

        new_pos = self.player.pos + rotated_offset
        self.rect = self.image.get_rect(center=new_pos)

        # Remove the sprite after its lifetime expires
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
    # ... (code is unchanged) ...
    def __init__(self, attack_type, attack_cooldown, combo_reset_time, attack_prefabs, attack_sprite_class=AttackSprite):
        self.attack_type = attack_type
        self.attack_cooldown = attack_cooldown
        self.combo_reset_time = combo_reset_time
        self.attack_prefabs = attack_prefabs
        self.attack_sprite_class = attack_sprite_class
# ... (rest of weapon definitions are unchanged) ...
# --- ======================= WEAPON DEFINITIONS ======================= ---
# MELEE
SWORD_SLASH_PREFAB = {"size": (15, 70), "color": WHITE, "lifetime": 150}
SWORD_THRUST_PREFAB = {"size": (10, 90), "color": WHITE, "lifetime": 250}
sword_weapon = WeaponData(
    attack_type='MELEE', attack_cooldown=300, combo_reset_time=800,
    attack_prefabs=[SWORD_SLASH_PREFAB, SWORD_SLASH_PREFAB, SWORD_THRUST_PREFAB]
)
SPEAR_THRUST_PREFAB = {"size": (10, 100), "color": WHITE, "lifetime": 200}
SPEAR_BARRAGE_PREFAB = {"size": (120, 120), "color": GREY, "lifetime": 100}
spear_weapon = WeaponData(
    attack_type='MELEE', attack_cooldown=250, combo_reset_time=600,
    attack_prefabs=[SPEAR_THRUST_PREFAB, SPEAR_THRUST_PREFAB, SPEAR_BARRAGE_PREFAB]
)
# RANGED
BOW_ARROW_PREFAB = {"speed": 25, "lifetime": 10000, "size": (10, 30), "color": WHITE}
bow_weapon = WeaponData(
    attack_type='RANGED', attack_cooldown=800, combo_reset_time=1000,
    attack_prefabs=[BOW_ARROW_PREFAB], attack_sprite_class=Projectile
)
WAND_SMALL_ORB_PREFAB = {"speed": 15, "lifetime": 3000, "size": (15, 15), "color": BLUE}
WAND_BIG_ORB_PREFAB = {"speed": 7, "lifetime": 4000, "size": (35, 35), "color": BLUE}
wand_weapon = WeaponData(
    attack_type='RANGED', attack_cooldown=400, combo_reset_time=900,
    attack_prefabs=[WAND_SMALL_ORB_PREFAB, WAND_SMALL_ORB_PREFAB, WAND_BIG_ORB_PREFAB],
    attack_sprite_class=Projectile
)
# LASER
STAFF_LASER_PREFAB = {"lifetime": 100}
staff_weapon = WeaponData(
    attack_type='LASER', attack_cooldown=100, combo_reset_time=0,
    attack_prefabs=[STAFF_LASER_PREFAB], attack_sprite_class=Laser
)
# A dictionary to easily access weapons by name
WEAPONS = {
    "sword": sword_weapon,
    "spear": spear_weapon,
    "bow": bow_weapon,
    "wand": wand_weapon,
    "staff": staff_weapon
}
