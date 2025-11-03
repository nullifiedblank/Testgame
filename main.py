import pygame
import sys
from settings import *
from player import Player
from weapon import WEAPONS # Import the dictionary of all weapons
from hud import HUD, Camera
from skills import DashSkill
from projectile import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top-Down Game")
        self.clock = pygame.time.Clock()

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # --- Easily change the equipped weapon here for testing ---
        self.player.current_weapon = WEAPONS["staff"]

        self.player.skills["dash"] = DashSkill(self.player)

        self.camera = Camera(2000, 2000)
        self.hud = HUD(self.player)

        self.attack_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

    def run(self):
        running = True
        is_attacking = False # To track continuous input for the laser

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # --- Handle Attack Input ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click press
                        is_attacking = True
                        # For non-laser weapons, attack is called once here
                        if self.player.current_weapon.attack_type != 'LASER':
                            self.player.attack(self.attack_sprites, self.projectile_sprites, True)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # Left click release
                        is_attacking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.activate_skill("dash")

            # --- For continuous attacks like the laser ---
            if self.player.current_weapon.attack_type == 'LASER':
                self.player.attack(self.attack_sprites, self.projectile_sprites, is_attacking)

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

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

if __name__ == "__main__":
    game = Game()
    game.run()
