import pygame
import sys
import math

# --- Initialization ---
pygame.init()

# --- Screen Settings ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Game")
clock = pygame.time.Clock()
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)

# --- Player Class ---
class Player:
    def __init__(self, x, y):
        # --- Visuals ---
        self.image_orig = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image_orig, RED, [(0, 40), (20, 0), (40, 40)])
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0

        # --- Stats ---
        self.speed = 5
        self.max_health = 200
        self.health = self.max_health
        self.max_energy = 200
        self.energy = self.max_energy

        # --- Weapon & Attack ---
        self.current_weapon = None
        self.combo_counter = 0
        self.last_attack_time = 0

        # --- Dash Skill ---
        self.is_dashing = False
        self.dash_speed = 30
        self.dash_duration = 100 # ms
        self.dash_cooldown = 4000 # ms
        self.dash_energy_cost = 15
        self.dash_start_time = 0
        self.last_dash_time = -self.dash_cooldown # Allow dashing from the start
        self.is_invulnerable = False

    def handle_input(self, keys, mouse_pos):
        # Player cannot move or aim while dashing
        if self.is_dashing:
            return

        # --- Movement ---
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y -= 1
        if keys[pygame.K_s]: move_vector.y += 1
        if keys[pygame.K_a]: move_vector.x -= 1
        if keys[pygame.K_d]: move_vector.x += 1

        if move_vector.length() > 0:
            move_vector.normalize_ip()
            self.rect.move_ip(move_vector * self.speed)

        # --- Aiming ---
        dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def attack(self, attack_sprites_group):
        if not self.current_weapon or self.is_dashing: return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.current_weapon.attack_cooldown: return

        if current_time - self.last_attack_time > self.current_weapon.combo_reset_time:
            self.combo_counter = 0

        attack_data = self.current_weapon.attack_prefabs[self.combo_counter]

        angle_rad = math.radians(self.angle + 90)
        spawn_pos = (self.rect.centerx + 60 * math.cos(angle_rad),
                     self.rect.centery - 60 * math.sin(angle_rad))

        attack_sprite = AttackSprite(pos=spawn_pos, rotation=self.angle, **attack_data)
        attack_sprites_group.add(attack_sprite)

        self.last_attack_time = current_time
        self.combo_counter = (self.combo_counter + 1) % len(self.current_weapon.attack_prefabs)

    def dash(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time > self.dash_cooldown:
            if self.energy >= self.dash_energy_cost:
                self.energy -= self.dash_energy_cost
                self.is_dashing = True
                self.is_invulnerable = True
                self.dash_start_time = current_time
                self.last_dash_time = current_time

    def update(self):
        if self.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time <= self.dash_duration:
                # Move player forward based on their current angle
                angle_rad = math.radians(self.angle + 90)
                move_vector = pygame.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
                self.rect.move_ip(move_vector * self.dash_speed)
            else:
                self.is_dashing = False
                self.is_invulnerable = False

# --- Weapon & Attack Classes ---
class AttackSprite(pygame.sprite.Sprite):
    # ... (rest of the classes are unchanged) ...
    def __init__(self, pos, rotation, size, color, lifetime):
        super().__init__()
        self.image_orig = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image_orig, color, (0, 0, *size))

        self.image = pygame.transform.rotate(self.image_orig, rotation)
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

class WeaponData:
    def __init__(self, attack_cooldown, combo_reset_time, attack_prefabs):
        self.attack_cooldown = attack_cooldown
        self.combo_reset_time = combo_reset_time
        self.attack_prefabs = attack_prefabs

# --- Weapon Definitions ---
SWORD_SLASH_PREFAB = {"size": (15, 70), "color": WHITE, "lifetime": 150}
SWORD_THRUST_PREFAB = {"size": (10, 90), "color": WHITE, "lifetime": 250}

sword_weapon = WeaponData(
    attack_cooldown=300, # ms
    combo_reset_time=800, # ms
    attack_prefabs=[SWORD_SLASH_PREFAB, SWORD_SLASH_PREFAB, SWORD_THRUST_PREFAB]
)

# --- Camera Class ---
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)
    def update(self, target_rect):
        x = -target_rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(SCREEN_HEIGHT / 2)
        self.camera.topleft = (x, y)

# --- HUD Class ---
class HUD:
    def __init__(self, player):
        self.player = player
        self.bar_length, self.bar_height = 200, 20
    def draw(self, surface):
        # Health Bar
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(surface, GREY, (10, SCREEN_HEIGHT - 30, self.bar_length, self.bar_height))
        pygame.draw.rect(surface, GREEN, (10, SCREEN_HEIGHT - 30, self.bar_length * health_ratio, self.bar_height))
        pygame.draw.rect(surface, WHITE, (10, SCREEN_HEIGHT - 30, self.bar_length, self.bar_height), 2)
        # Energy Bar
        energy_ratio = self.player.energy / self.player.max_energy
        pygame.draw.rect(surface, GREY, (10, SCREEN_HEIGHT - 60, self.bar_length, self.bar_height))
        pygame.draw.rect(surface, BLUE, (10, SCREEN_HEIGHT - 60, self.bar_length * energy_ratio, self.bar_height))
        pygame.draw.rect(surface, WHITE, (10, SCREEN_HEIGHT - 60, self.bar_length, self.bar_height), 2)

# --- Game Loop ---
def main():
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.current_weapon = sword_weapon

    camera = Camera(2000, 2000)
    hud = HUD(player)

    attack_sprites = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.attack(attack_sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.dash()

        keys = pygame.key.get_pressed()
        mouse_screen_pos = pygame.mouse.get_pos()
        mouse_world_pos = (mouse_screen_pos[0] - camera.camera.x, mouse_screen_pos[1] - camera.camera.y)

        player.handle_input(keys, mouse_world_pos)

        player.update() # Update player state (like dashing)
        camera.update(player.rect)
        attack_sprites.update()

        screen.fill(BLACK)

        screen.blit(player.image, camera.apply(player.rect))
        for sprite in attack_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        hud.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
