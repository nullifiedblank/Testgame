import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.color = GREY
        self.hover_color = (100, 100, 100) # A lighter grey for hover
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                return True # Button was clicked
        return False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2) # Border
        surface.blit(self.text_surf, self.text_rect)
