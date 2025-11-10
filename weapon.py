import pygame
import math
from projectile import Projectile
from settings import RED

# ... (WeaponAnimation is unchanged) ...
class WeaponAnimation:
    def __init__(self, weapon_sprite, anim_data, hittable_sprites):
        self.weapon_sprite = weapon_sprite; self.anim_data = anim_data; self.hittable_sprites = hittable_sprites
        self.start_time = pygame.time.get_ticks(); self.duration = anim_data.get('duration', 300); self.is_done = False
        self.hit_targets = []
    def update(self):
        progress = (pygame.time.get_ticks() - self.start_time) / self.duration
        if progress >= 1: self.is_done = True; progress = 1
        if self.anim_data.get('type') == 'slash':
            start_angle = self.anim_data.get('start_angle', 60); end_angle = self.anim_data.get('end_angle', -90)
            current_angle = start_angle + (end_angle - start_angle) * progress
            self.weapon_sprite.set_anim_rotation(current_angle)
        elif self.anim_data.get('type') == 'thrust':
            start_offset = self.anim_data.get('start_offset', 0); end_offset = self.anim_data.get('end_offset', 40)
            if progress < 0.5: current_offset = start_offset + (end_offset - start_offset) * (progress * 2)
            else: current_offset = end_offset - (end_offset - start_offset) * ((progress - 0.5) * 2)
            self.weapon_sprite.set_anim_offset(current_offset)
        collided_sprites = pygame.sprite.spritecollide(self.weapon_sprite, self.hittable_sprites, False, pygame.sprite.collide_mask)
        for sprite in collided_sprites:
            if hasattr(sprite, 'health') and sprite not in self.hit_targets:
                sprite.health.take_damage(self.anim_data.get('damage', 0))

                # --- Talisman Integration ---
                if self.weapon_sprite.player.talisman:
                    has_slow = self.anim_data.get('has_slow', False)
                    self.weapon_sprite.player.talisman.on_deal_damage(self.weapon_sprite.player, sprite, has_slow)

                self.hit_targets.append(sprite)

class HeldWeapon(pygame.sprite.Sprite):
    def __init__(self, player, image):
        super().__init__()
        self.player = player
        self.image_orig = image
        self.image = self.image_orig
        self.base_angle = 0
        self.anim_angle_offset = 0
        self.anim_pos_offset = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect(center=player.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def set_anim_rotation(self, angle_offset):
        self.anim_angle_offset = angle_offset

    def set_anim_offset(self, offset_val):
        self.anim_pos_offset = pygame.math.Vector2(offset_val, 0)

    def update(self, *args, **kwargs):
        # Apply melee animation angle offset
        self.base_angle = self.player.angle
        final_angle = self.base_angle + self.anim_angle_offset + 45

        # Perform the rotation and positioning logic as specified
        self.image = pygame.transform.rotate(self.image_orig, final_angle)

        anchor = pygame.math.Vector2(15, 48)
        center = pygame.math.Vector2(self.image_orig.get_width() / 2, self.image_orig.get_height() / 2)
        offset = anchor - center
        rotated_offset = offset.rotate(-final_angle)

        # The blit position is the player's center minus the rotated offset
        # Note: self.rect.center will be used for blitting, so we set that
        self.rect = self.image.get_rect(center=self.player.rect.center - rotated_offset)

        # This part handles the melee 'thrust' animation, it must be applied last
        if self.anim_pos_offset.length() > 0:
            angle_rad = math.radians(self.base_angle + 90)
            move_vector = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * self.anim_pos_offset.x
            self.rect.move_ip(move_vector)

        self.mask = pygame.mask.from_surface(self.image)


# ... (Laser, WeaponData, and WEAPONS definitions are unchanged) ...
class Laser(pygame.sprite.Sprite):
    def __init__(self, player, lifetime, damage):
        super().__init__()
        self.player = player
        self.lifetime = lifetime
        self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
        self.is_laser = True
        self.current_angle = self.player.angle
        self.start_pos = self.player.pos
        angle_rad = math.radians(self.current_angle + 90)
        self.end_pos = self.start_pos + pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * 2000
        # Add a dummy image and rect to prevent rendering crashes
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=player.pos)
    def update(self, hittable_sprites):
        target_angle = self.player.angle
        self.current_angle += (target_angle - self.current_angle) * 0.01 # Interpolate angle

        self.start_pos = self.player.pos
        angle_rad = math.radians(self.current_angle + 90)
        self.end_pos = self.start_pos + pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) * 2000

        for sprite in hittable_sprites:
            if hasattr(sprite, 'health') and sprite.rect.clipline(self.start_pos, self.end_pos):
                sprite.health.take_damage(self.damage * 0.1)

                # --- Talisman Integration ---
                if self.player.talisman:
                    self.player.talisman.on_deal_damage(self.player, sprite, False)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime: self.kill()
class WeaponData:
    def __init__(self, held_image_path, attack_type, attack_cooldown, combo_reset_time, attack_data, attack_sprite_class=None, **kwargs):
        self.held_image_path = held_image_path; self.attack_type = attack_type
        self.attack_cooldown = attack_cooldown; self.combo_reset_time = combo_reset_time
        self.attack_data = attack_data; self.attack_sprite_class = attack_sprite_class
        self.extra_assets_paths = kwargs
sword_weapon = WeaponData( held_image_path="assets/weapons/sword.png", attack_type='MELEE', attack_cooldown=400, combo_reset_time=900, attack_data=[{'type': 'slash', 'duration': 150, 'damage': 15, 'start_angle': 60, 'end_angle': -90}]*2 + [{'type': 'thrust', 'duration': 150, 'damage': 25, 'start_offset': 0, 'end_offset': 50}] )
spear_weapon = WeaponData( held_image_path="assets/weapons/spear.png", attack_type='MELEE', attack_cooldown=600, combo_reset_time=1500, attack_data=[
    {'type': 'thrust', 'duration': 250, 'damage': 20, 'start_offset': 0, 'end_offset': 60},
    {'type': 'thrust', 'duration': 250, 'damage': 20, 'start_offset': 0, 'end_offset': 60},
    {'multi_hit': [
        {'type': 'thrust', 'duration': 100, 'damage': 10, 'start_offset': 0, 'end_offset': 40},
        {'type': 'thrust', 'duration': 100, 'damage': 10, 'start_offset': 0, 'end_offset': 40},
        {'type': 'thrust', 'duration': 100, 'damage': 10, 'start_offset': 0, 'end_offset': 40},
    ]}
])
bow_weapon = WeaponData( held_image_path="assets/weapons/bow.png", attack_type='RANGED', attack_cooldown=800, combo_reset_time=1000, attack_data=[{"image_path": "assets/projectiles/arrow.png", "speed": 25, "lifetime": 10000, "damage": 40}], attack_sprite_class=Projectile, bow_draw_image="assets/weapons/bow_draw.png", bow_empty_image="assets/weapons/bow_empty.png")
wand_weapon = WeaponData( held_image_path="assets/weapons/wand.png", attack_type='RANGED', attack_cooldown=400, combo_reset_time=900, attack_data=[
    {"image_path": "assets/projectiles/small_orb.png", "speed": 15, "lifetime": 3000, "damage": 10},
    {"image_path": "assets/projectiles/small_orb.png", "speed": 15, "lifetime": 3000, "damage": 10},
    {"image_path": "assets/projectiles/big_orb.png", "speed": 7, "lifetime": 4000, "damage": 25, "has_slow": True}
], attack_sprite_class=Projectile )
staff_weapon = WeaponData( held_image_path="assets/weapons/staff.png", attack_type='LASER', attack_cooldown=100, combo_reset_time=0, attack_data=[{"lifetime": 100, "damage": 5}], attack_sprite_class=Laser )
WEAPONS = { "sword": sword_weapon, "spear": spear_weapon, "bow": bow_weapon, "wand": wand_weapon, "staff": staff_weapon }
