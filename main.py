import pygame
import sys
from settings import *
from game_screen import GameScreen
from ui import Button
from weapon import WEAPONS # Import the WEAPONS dictionary

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_state = 'main_menu'

        self.game_screen = None
        self.selected_weapon = "sword" # Default weapon

        # --- Menu Buttons ---
        self.play_button = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 60, 200, 50, 'Play')
        self.settings_button = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2, 200, 50, 'Settings')
        self.quit_button = Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 60, 200, 50, 'Quit')
        self.menu_buttons = [self.play_button, self.settings_button, self.quit_button]

        # --- Loadout Buttons ---
        self.loadout_buttons = []
        button_y = SCREEN_HEIGHT / 4
        for weapon_key in WEAPONS.keys():
            button = Button(SCREEN_WIDTH / 2 - 150, button_y, 300, 50, weapon_key.title())
            self.loadout_buttons.append(button)
            button_y += 60

    def run(self):
        while True:
            if self.game_state == 'main_menu':
                self.game_state = self.main_menu_loop()
            elif self.game_state == 'loadout_selection':
                self.game_state = self.loadout_loop()
            elif self.game_state == 'gameplay':
                # Create a new game screen instance each time we play
                self.game_screen = GameScreen(self.screen, self.clock)
                self.game_screen.set_weapon(self.selected_weapon)
                self.game_state = self.game_screen.run()
            elif self.game_state == 'quit':
                pygame.quit()
                sys.exit()

    def main_menu_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if self.play_button.handle_event(event): return 'loadout_selection'
            if self.settings_button.handle_event(event): pass # Placeholder
            if self.quit_button.handle_event(event): return 'quit'

        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 70)
        title_surf = font.render("My Game", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        self.screen.blit(title_surf, title_rect)
        for button in self.menu_buttons:
            button.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
        return 'main_menu'

    def loadout_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'main_menu' # Go back to main menu

            for i, button in enumerate(self.loadout_buttons):
                if button.handle_event(event):
                    self.selected_weapon = list(WEAPONS.keys())[i]
                    return 'gameplay'

        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 50)
        title_surf = font.render("Choose Your Weapon", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH/2, 100))
        self.screen.blit(title_surf, title_rect)
        for button in self.loadout_buttons:
            button.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
        return 'loadout_selection'

if __name__ == "__main__":
    app = App()
    app.run()
