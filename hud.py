import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)
    def update(self, target_rect):
        x = -target_rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(SCREEN_HEIGHT / 2)
        self.camera.topleft = (x, y)

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 22)
        self.bar_length, self.bar_height = 200, 20
        self.bar_margin = 10

    def draw(self, surface):
        # --- Health Bar ---
        health_bar_x = self.bar_margin
        health_bar_y = self.bar_margin

        health_ratio = self.player.health / self.player.max_health
        health_fill_width = int(self.bar_length * health_ratio)

        health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, self.bar_length, self.bar_height)
        health_fill_rect = pygame.Rect(health_bar_x, health_bar_y, health_fill_width, self.bar_height)

        pygame.draw.rect(surface, GREY, health_bar_rect)
        pygame.draw.rect(surface, GREEN, health_fill_rect)
        pygame.draw.rect(surface, WHITE, health_bar_rect, 2)

        # --- Energy Bar ---
        energy_bar_y = health_bar_y + self.bar_height + self.bar_margin

        energy_ratio = self.player.energy / self.player.max_energy
        energy_fill_width = int(self.bar_length * energy_ratio)

        energy_bar_rect = pygame.Rect(health_bar_x, energy_bar_y, self.bar_length, self.bar_height)
        energy_fill_rect = pygame.Rect(health_bar_x, energy_bar_y, energy_fill_width, self.bar_height)

        pygame.draw.rect(surface, GREY, energy_bar_rect)
        pygame.draw.rect(surface, BLUE, energy_fill_rect)
        pygame.draw.rect(surface, WHITE, energy_bar_rect, 2)

        # --- Text Display ---
        health_text = f"{int(self.player.health)} / {self.player.max_health}"
        energy_text = f"{int(self.player.energy)} / {self.player.max_energy}"

        health_text_surf = self.font.render(health_text, True, WHITE)
        energy_text_surf = self.font.render(energy_text, True, WHITE)

        health_text_rect = health_text_surf.get_rect(center=health_bar_rect.center)
        energy_text_rect = energy_text_surf.get_rect(center=energy_bar_rect.center)

        surface.blit(health_text_surf, health_text_rect)
        surface.blit(energy_text_surf, energy_text_rect)
