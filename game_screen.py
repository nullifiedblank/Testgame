import pygame
import sys
from settings import *
from player import Player
from weapon import WEAPONS
from hud import HUD, Camera
from skills import DashSkill
from projectile import Projectile

class GameScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player.skills["dash"] = DashSkill(self.player)

        self.camera = Camera(2000, 2000) # Re-enable the camera
        self.hud = HUD(self.player)

        self.all_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

    def set_weapon(self, weapon_key):
        self.player.set_weapon(WEAPONS[weapon_key])
        if self.player.held_weapon:
            self.all_sprites.add(self.player.held_weapon)

    def run(self):
        running = True
        is_attacking = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'main_menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_attacking = True
                        if self.player.current_weapon_data and self.player.current_weapon_data.attack_type != 'LASER':
                            self.player.attack(self.attack_sprites, self.projectile_sprites, True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: is_attacking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: self.player.activate_skill("dash")
                    if event.key == pygame.K_ESCAPE: return 'main_menu'

            self.update(is_attacking)
            self.draw()

    def update(self, is_attacking):
        keys = pygame.key.get_pressed()
        mouse_screen_pos = pygame.mouse.get_pos()
        # Calculate mouse position relative to the camera view
        mouse_world_pos = (mouse_screen_pos[0] - self.camera.camera.x, mouse_screen_pos[1] - self.camera.camera.y)

        self.player.handle_input(keys, mouse_world_pos)
        self.player.update()

        if self.player.current_weapon_data and self.player.current_weapon_data.attack_type == 'LASER':
            self.player.attack(self.attack_sprites, self.projectile_sprites, is_attacking)

        self.camera.update(self.player.rect) # Re-enable camera updates
        self.all_sprites.update()
        self.attack_sprites.update()
        self.projectile_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw all sprites with camera offset
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        if self.player.held_weapon:
            self.screen.blit(self.player.held_weapon.image, self.camera.apply(self.player.held_weapon.rect))
        for sprite in self.attack_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.projectile_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # Draw the HUD last, without camera offset
        self.hud.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
