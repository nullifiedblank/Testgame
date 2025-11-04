import pygame
import sys
from settings import *
from player import Player
from weapon import WEAPONS
from hud import HUD, Camera
from skills import DashSkill
from background import create_checkerboard # Import the new function

class GameScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        # --- World & Camera ---
        self.world_width, self.world_height = 2000, 2000
        self.background = create_checkerboard(self.world_width, self.world_height, 100)
        self.camera = Camera(self.world_width, self.world_height)

        # --- Player & HUD ---
        self.player = Player(self.world_width // 2, self.world_height // 2)
        self.player.skills["dash"] = DashSkill(self.player)
        self.hud = HUD(self.player)

        # --- Sprite Groups ---
        self.all_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

    def set_weapon(self, weapon_key):
        self.player.set_weapon(WEAPONS[weapon_key], self.all_sprites)

    def run(self):
        # ... (run loop is unchanged) ...
        running = True
        is_attacking = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'main_menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_attacking = True
                        if self.player.weapon and self.player.weapon.attack_type != 'LASER':
                            self.player.attack(self.all_sprites, self.projectile_sprites, True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: is_attacking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: self.player.activate_skill("dash")
                    if event.key == pygame.K_ESCAPE: return 'main_menu'
            self.update(is_attacking)
            self.draw()

    def update(self, is_attacking):
        # ... (update logic is unchanged) ...
        keys = pygame.key.get_pressed()
        mouse_screen_pos = pygame.mouse.get_pos()
        mouse_world_pos = (mouse_screen_pos[0] - self.camera.camera.x, mouse_screen_pos[1] - self.camera.camera.y)
        self.player.handle_input(keys, mouse_world_pos)
        self.player.update()
        if self.player.weapon and self.player.weapon.attack_type == 'LASER':
            self.player.attack(self.all_sprites, self.projectile_sprites, is_attacking)
        self.camera.update(self.player.rect)
        self.all_sprites.update()
        self.projectile_sprites.update()

    def draw(self):
        # Draw the tiled background first, offset by the camera
        self.screen.blit(self.background, self.camera.apply(pygame.Rect(0, 0, self.world_width, self.world_height)))

        # Draw player
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # Draw all other sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.projectile_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # Draw HUD last (not affected by camera)
        self.hud.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
