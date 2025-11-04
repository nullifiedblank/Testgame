import pygame
import os
from settings import RED

class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_image(self, file_path, size=(64, 64)):
        script_dir = os.path.dirname(__file__)
        abs_path = os.path.join(script_dir, file_path)
        try:
            image = pygame.image.load(abs_path).convert_alpha()
            return pygame.transform.scale(image, size)
        except pygame.error as e:
            print(f"Error loading image: {file_path} - {e}")
            placeholder = pygame.Surface(size)
            placeholder.fill(RED)
            return placeholder

    def load_assets(self):
        print("Loading assets...")

        # Player
        self.assets['player'] = self.load_image('assets/character/player.png')

        # Weapons
        self.assets['assets/weapons/sword.png'] = self.load_image('assets/weapons/sword.png')
        self.assets['assets/weapons/spear.png'] = self.load_image('assets/weapons/spear.png')
        self.assets['assets/weapons/bow.png'] = self.load_image('assets/weapons/bow.png')
        self.assets['assets/weapons/bow_draw.png'] = self.load_image('assets/weapons/bow_draw.png')
        self.assets['assets/weapons/bow_empty.png'] = self.load_image('assets/weapons/bow_empty.png')
        self.assets['assets/weapons/wand.png'] = self.load_image('assets/weapons/wand.png')
        self.assets['assets/weapons/staff.png'] = self.load_image('assets/weapons/staff.png')

        # Projectiles
        self.assets['assets/projectiles/arrow.png'] = self.load_image('assets/projectiles/arrow.png')
        self.assets['assets/projectiles/small_orb.png'] = self.load_image('assets/projectiles/small_orb.png')
        self.assets['assets/projectiles/big_orb.png'] = self.load_image('assets/projectiles/big_orb.png')
        self.assets['assets/projectiles/enemy_bullet.png'] = self.load_image('assets/projectiles/enemy_bullet.png', size=(20, 20))

        # Enemies
        self.assets['assets/enemies/turret.png'] = self.load_image('assets/enemies/turret.png')

        print("...assets loaded.")

    def get(self, key):
        return self.assets.get(key)
