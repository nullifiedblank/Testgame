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

        self.camera = Camera(2000, 2000)
        self.hud = HUD(self.player)

        self.attack_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

    def set_weapon(self, weapon_key):
        """Sets the player's weapon based on a key from the WEAPONS dictionary."""
        self.player.current_weapon = WEAPONS[weapon_key]

    def run(self):
        running = True
        is_attacking = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Instead of quitting, we'll return to the main menu
                    return 'main_menu'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_attacking = True
                        if self.player.current_weapon.attack_type != 'LASER':
                            self.player.attack(self.attack_sprites, self.projectile_sprites, True)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        is_attacking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.activate_skill("dash")
                    if event.key == pygame.K_ESCAPE: # Allow Esc to return to menu
                        return 'main_menu'

            if self.player.current_weapon and self.player.current_weapon.attack_type == 'LASER':
                self.player.attack(self.attack_sprites, self.projectile_sprites, is_attacking)

            self.update()
            self.draw()

    def update(self):
        keys = pygame.key.get_pressed()
        mouse_screen_pos = pygame.mouse.get_pos()
        mouse_world_pos = (mouse_screen_pos[0] - self.camera.camera.x, mouse_screen_pos[1] - self.camera.camera.y)

        self.player.handle_input(keys, mouse_world_pos)
        self.player.update()

        self.camera.update(self.player.rect)
        self.attack_sprites.update()
        self.projectile_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)

        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        for sprite in self.attack_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.projectile_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        self.hud.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
