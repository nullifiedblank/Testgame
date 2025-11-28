import unittest
import pygame
from player import Player
from weapon import WEAPONS
from assets import AssetManager

# Mock the AssetManager to avoid loading real assets in a headless environment
class MockAssetManager:
    def get(self, name):
        # Return a dummy surface for any sprite request
        return pygame.Surface((32, 32))

class TestPlayer(unittest.TestCase):
    def test_equip_weapon(self):
        pygame.init()
        # Use the mock asset manager to isolate the Player class from the filesystem
        asset_manager = MockAssetManager()
        player = Player(100, 100, asset_manager)

        # Test equipping a weapon from the predefined WEAPONS dictionary
        weapon_key = 'sword'
        weapon_data = WEAPONS[weapon_key]
        all_sprites = pygame.sprite.Group()

        player.set_weapon(weapon_data, all_sprites)

        # Assert that the weapon was equipped correctly
        self.assertIsNotNone(player.weapon)
        self.assertIsNotNone(player.held_weapon) # Also check the held_weapon sprite
        self.assertIn(player.held_weapon, all_sprites) # Correctly check for the sprite
        self.assertEqual(player.weapon, weapon_data) # Check that the data is set

if __name__ == '__main__':
    # Set a dummy video driver for headless testing environments
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    unittest.main()
