import pygame
import sys
from settings import *
from player import Player
from weapon import WEAPONS
from hud import HUD, Camera
from skills import DashSkill
from background import create_checkerboard
from enemy import Turret # Import the Turret class

class GameScreen:
    def __init__(self, screen, clock):
        self.screen = screen; self.clock = clock

        # --- World & Camera ---
        self.world_width, self.world_height = 2000, 2000
        self.background = create_checkerboard(self.world_width, self.world_height, 100)
        self.camera = Camera(self.world_width, self.world_height)

        # --- Player & HUD ---
        self.player = Player(self.world_width // 2, self.world_height // 2)
        self.player.skills["dash"] = DashSkill(self.player)
        self.hud = HUD(self.player)

        # --- Sprite Groups ---
        self.all_sprites = pygame.sprite.Group() # Holds player's weapon and laser beams
        self.projectile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # --- Enemy Management ---
        self.turret_spawn_pos = (self.world_width // 2 + 300, self.world_height // 2)
        self.turret_death_time = 0
        self.turret_respawn_delay = 5000 # 5 seconds
        self.spawn_turret()

    def set_weapon(self, weapon_key):
        self.player.set_weapon(WEAPONS[weapon_key], self.all_sprites)

    def spawn_turret(self):
        turret = Turret(self.turret_spawn_pos[0], self.turret_spawn_pos[1], self.player)
        self.enemy_sprites.add(turret)
        self.turret_instance = turret # Keep a direct reference for checking death

    def run(self):
        # ... (run loop is unchanged) ...
        running = True; is_attacking = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'main_menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_attacking = True
                        if self.player.weapon and self.player.weapon.attack_type != 'LASER':
                            self.player.attack(self.enemy_sprites, self.projectile_sprites, True)
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
        mouse_world_pos = (mouse_screen_pos[0] - self.camera.camera.x, mouse_screen_pos[1] - self.camera.camera.y)

        self.player.handle_input(keys, mouse_world_pos)
        self.player.update()

        if self.player.weapon and self.player.weapon.attack_type == 'LASER':
            self.player.attack(self.enemy_sprites, self.projectile_sprites, is_attacking)

        # Update sprites, passing the correct groups for collision
        self.camera.update(self.player.rect)
        self.all_sprites.update(self.enemy_sprites) # Pass enemies to laser/melee
        self.projectile_sprites.update(self.enemy_sprites) # Pass enemies to projectiles
        self.enemy_sprites.update(self.projectile_sprites) # Pass projectiles to enemies

        # --- Check for Turret Death and Respawn ---
        if not self.turret_instance.alive() and self.turret_death_time == 0:
            self.turret_death_time = pygame.time.get_ticks()

        if self.turret_death_time != 0 and pygame.time.get_ticks() - self.turret_death_time > self.turret_respawn_delay:
            self.spawn_turret()
            self.turret_death_time = 0


    def draw(self):
        # ... (draw is mostly unchanged) ...
        self.screen.blit(self.background, self.camera.apply(pygame.Rect(0, 0, self.world_width, self.world_height)))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.projectile_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.enemy_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        self.hud.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
