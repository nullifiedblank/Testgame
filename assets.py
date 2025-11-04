import pygame
import os
from settings import RED

# A global dictionary to hold all loaded image assets
ASSETS = {}

def load_image(file_path, size=(64, 64)):
    """A centralized function to load and scale images, ensuring paths are correct."""
    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, file_path)
    try:
        image = pygame.image.load(abs_path).convert_alpha()
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image: {file_path} - {e}")
        # Return a placeholder if the image fails to load for any reason
        placeholder = pygame.Surface(size)
        placeholder.fill(RED)
        return placeholder

def init_assets():
    """Loads all game assets into the global ASSETS dictionary."""
    print("Loading assets...")

    # Player
    ASSETS['player'] = load_image('assets/character/player.png')

    # Weapons
    ASSETS['assets/weapons/sword.png'] = load_image('assets/weapons/sword.png')
    ASSETS['assets/weapons/spear.png'] = load_image('assets/weapons/spear.png')
    ASSETS['assets/weapons/bow.png'] = load_image('assets/weapons/bow.png')
    ASSETS['assets/weapons/bow_draw.png'] = load_image('assets/weapons/bow_draw.png')
    ASSETS['assets/weapons/bow_empty.png'] = load_image('assets/weapons/bow_empty.png')
    ASSETS['assets/weapons/wand.png'] = load_image('assets/weapons/wand.png')
    ASSETS['assets/weapons/staff.png'] = load_image('assets/weapons/staff.png')

    # Projectiles
    ASSETS['assets/projectiles/arrow.png'] = load_image('assets/projectiles/arrow.png')
    ASSETS['assets/projectiles/small_orb.png'] = load_image('assets/projectiles/small_orb.png')
    ASSETS['assets/projectiles/big_orb.png'] = load_image('assets/projectiles/big_orb.png')
    ASSETS['assets/projectiles/enemy_bullet.png'] = load_image('assets/projectiles/enemy_bullet.png', size=(20, 20))

    # Enemies
    ASSETS['assets/enemies/turret.png'] = load_image('assets/enemies/turret.png')

    print("...assets loaded.")
