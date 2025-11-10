import pygame
import sys
import settings
from player import Player
from background import create_checkerboard
from weapon import WEAPONS
from hud import HUD, Camera
from skills import DashSkill
from enemy import Turret

class GameScreen:
    def __init__(self, screen, clock, asset_manager):
        self.screen = screen
        self.clock = clock
        self.asset_manager = asset_manager

        # --- World & Camera ---
        self.world_width, self.world_height = 2000, 2000
        self.background = create_checkerboard(self.world_width, self.world_height, 100)
        self.camera = Camera(self.world_width, self.world_height)

        # --- Sprite Groups ---
        self.all_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # --- Game Objects ---
        self.player = Player(self.world_width // 2, self.world_height // 2, self.asset_manager)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.player.skills["dash"] = DashSkill(self.player, self.all_sprites)
        self.hud = HUD(self.player)
        self.font = pygame.font.Font(None, 22)

        self.turret_spawn_pos = (self.world_width // 2 + 300, self.world_height // 2)
        self.turret_death_time = 0
        self.turret_respawn_delay = 5000
        self.spawn_turret()

    def set_weapon(self, weapon_key):
        self.player.set_weapon(WEAPONS[weapon_key], self.all_sprites)

    def spawn_turret(self):
        turret = Turret(self.turret_spawn_pos[0], self.turret_spawn_pos[1], self.player, self.asset_manager)
        self.enemy_sprites.add(turret)
        self.turret_instance = turret

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
                            self.player.attack(self.all_sprites, self.enemy_sprites, self.projectile_sprites, True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: is_attacking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: self.player.activate_skill("dash")
                    if event.key == pygame.K_ESCAPE: return 'main_menu'
                    if event.key == pygame.K_h:
                        settings.DEBUG_HITBOXES = not settings.DEBUG_HITBOXES
            self.update(is_attacking)
            self.draw()

    def update(self, is_attacking):
        # ... (update logic is unchanged) ...
        keys = pygame.key.get_pressed()
        mouse_screen_pos = pygame.mouse.get_pos()
        mouse_world_pos = (mouse_screen_pos[0] - self.camera.camera.x, mouse_screen_pos[1] - self.camera.camera.y)
        self.player.handle_input(keys, mouse_world_pos)
        self.player.update()
        if self.player.weapon and self.player.weapon.attack_type in ['LASER', 'RANGED_CHARGE']:
            self.player.attack(self.all_sprites, self.enemy_sprites, self.projectile_sprites, is_attacking)
        self.camera.update(self.player.rect)

        # Update sprites
        self.all_sprites.update(self.enemy_sprites) # General updates
        self.projectile_sprites.update(self.enemy_sprites, self.player_group) # Check projectile collisions
        self.enemy_sprites.update(self.all_sprites, self.projectile_sprites) # Update enemies

        if not self.turret_instance.alive() and self.turret_death_time == 0:
            self.turret_death_time = pygame.time.get_ticks()
        if self.turret_death_time != 0 and pygame.time.get_ticks() - self.turret_death_time > self.turret_respawn_delay:
            self.spawn_turret()
            self.turret_death_time = 0

    def draw(self):
        # ... (draw is unchanged) ...
        self.screen.blit(self.background, self.camera.apply(pygame.Rect(0, 0, self.world_width, self.world_height)))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.projectile_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        for sprite in self.enemy_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
            # Draw HP text
            hp_text = f"{int(sprite.health.current_hp)} / {sprite.health.max_hp}"
            text_surf = self.font.render(hp_text, True, settings.WHITE)
            text_rect = text_surf.get_rect(center=self.camera.apply(sprite.rect).center - pygame.math.Vector2(0, sprite.rect.height / 2 + 10))
            self.screen.blit(text_surf, text_rect)

        if settings.DEBUG_HITBOXES:
            # Draw player mask outline
            player_mask_surf = self.player.mask.to_surface(setcolor=(255, 0, 0, 200), unsetcolor=(0,0,0,0))
            self.screen.blit(player_mask_surf, self.camera.apply(self.player.rect))

            # Draw held weapon mask outline
            if self.player.held_weapon:
                weapon_mask_surf = self.player.held_weapon.mask.to_surface(setcolor=(255, 165, 0, 200), unsetcolor=(0,0,0,0))
                self.screen.blit(weapon_mask_surf, self.camera.apply(self.player.held_weapon.rect))

            # Draw enemy rects (since they use rect-based collision)
            for sprite in self.enemy_sprites:
                pygame.draw.rect(self.screen, (0, 255, 0), self.camera.apply(sprite.rect), 2)

            # Draw projectile rects
            for sprite in self.projectile_sprites:
                pygame.draw.rect(self.screen, (0, 0, 255), self.camera.apply(sprite.rect), 2)

            # Draw laser line
            for sprite in self.all_sprites:
                if hasattr(sprite, 'is_laser') and sprite.is_laser:
                    start_pos_cam = self.camera.apply_point(sprite.start_pos)
                    end_pos_cam = self.camera.apply_point(sprite.end_pos)
                    pygame.draw.line(self.screen, (255, 0, 255), start_pos_cam, end_pos_cam, 3)

        self.hud.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(settings.FPS)
