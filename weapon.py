import pygame
import math
from projectile import Projectile
from settings import RED

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
                self.hit_targets.append(sprite)

class HeldWeapon(pygame.sprite.Sprite):
    def __init__(self, player, image):
        super().__init__(); self.player = player; self.image_orig = image; self.image = self.image_orig
        self.base_angle = 0; self.anim_angle_offset = 0; self.anim_pos_offset = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect(center=player.rect.center); self.mask = pygame.mask.from_surface(self.image)
    def set_anim_rotation(self, angle_offset): self.anim_angle_offset = angle_offset
    def set_anim_offset(self, offset_val): self.anim_pos_offset = pygame.math.Vector2(offset_val, 0)
    def update(self, *args, **kwargs):
        self.base_angle = self.player.angle; final_angle = self.base_angle + self.anim_angle_offset
        self.image = pygame.transform.rotate(self.image_orig, final_angle)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.player.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        rotated_pos_offset = self.anim_pos_offset.rotate(-self.base_angle)
        self.rect.move_ip(rotated_pos_offset)

class Laser(pygame.sprite.Sprite):
    def __init__(self, player, lifetime, damage):
        super().__init__(); self.player = player; self.lifetime = lifetime; self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
    def update(self, hittable_sprites):
        end_pos = self.player.pos + pygame.math.Vector2(1, 0).rotate(-self.player.angle) * 2000
        collided_sprites = pygame.sprite.spritecollide(self.player, hittable_sprites, False, pygame.sprite.collide_line((self.player.pos.x, self.player.pos.y), (end_pos.x, end_pos.y)))
        for sprite in collided_sprites:
            if hasattr(sprite, 'health'):
                sprite.health.take_damage(self.damage * 0.1)
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime: self.kill()

class WeaponData:
    def __init__(self, held_image_path, attack_type, attack_cooldown, combo_reset_time, attack_data, attack_sprite_class=None, **kwargs):
        self.held_image_path = held_image_path
        self.attack_type = attack_type
        self.attack_cooldown = attack_cooldown
        self.combo_reset_time = combo_reset_time
        self.attack_data = attack_data
        self.attack_sprite_class = attack_sprite_class
        self.extra_assets_paths = kwargs

# --- WEAPON DEFINITIONS ---
sword_weapon = WeaponData( held_image_path="assets/weapons/sword.png", attack_type='MELEE', attack_cooldown=400, combo_reset_time=900, attack_data=[{'type': 'slash', 'duration': 300, 'damage': 15, 'start_angle': 60, 'end_angle': -90}]*2 + [{'type': 'thrust', 'duration': 400, 'damage': 25, 'start_offset': 0, 'end_offset': 50}] )
spear_weapon = WeaponData( held_image_path="assets/weapons/spear.png", attack_type='MELEE', attack_cooldown=300, combo_reset_time=700, attack_data=[{'type': 'thrust', 'duration': 250, 'damage': 20, 'start_offset': 0, 'end_offset': 60}]*2 + [{'type': 'slash', 'duration': 500, 'damage': 30, 'start_angle': 90, 'end_angle': -90}] )
bow_weapon = WeaponData( held_image_path="assets/weapons/bow.png", attack_type='RANGED', attack_cooldown=800, combo_reset_time=1000, attack_data=[{"image_path": "assets/projectiles/arrow.png", "speed": 25, "lifetime": 10000, "damage": 40}], attack_sprite_class=Projectile, bow_draw_image="assets/weapons/bow_draw.png", bow_empty_image="assets/weapons/bow_empty.png")
wand_weapon = WeaponData( held_image_path="assets/weapons/wand.png", attack_type='RANGED', attack_cooldown=400, combo_reset_time=900, attack_data=[{"image_path": "assets/projectiles/small_orb.png", "speed": 15, "lifetime": 3000, "damage": 10}] * 2 + [{"image_path": "assets/projectiles/big_orb.png", "speed": 7, "lifetime": 4000, "damage": 25}], attack_sprite_class=Projectile )
staff_weapon = WeaponData( held_image_path="assets/weapons/staff.png", attack_type='LASER', attack_cooldown=100, combo_reset_time=0, attack_data=[{"lifetime": 100, "damage": 5}], attack_sprite_class=Laser )
WEAPONS = { "sword": sword_weapon, "spear": spear_weapon, "bow": bow_weapon, "wand": wand_weapon, "staff": staff_weapon }
