import pygame

class Skill:
    def __init__(self, player, cooldown, energy_cost):
        self.player = player
        self.cooldown = cooldown
        self.energy_cost = energy_cost
        self.last_used_time = -cooldown # Allow use from the start

    def can_use(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_used_time > self.cooldown and
                self.player.energy >= self.energy_cost)

    def activate(self):
        if self.can_use():
            self.player.energy -= self.energy_cost
            self.last_used_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        # Most skills won't have a continuous update, but some might
        pass

class DashSkill(Skill):
    def __init__(self, player):
        super().__init__(player, cooldown=4000, energy_cost=15)
        self.dash_speed = 30
        self.dash_duration = 100 # ms
        self.dash_start_time = 0

    def activate(self):
        if super().activate():
            self.player.is_dashing = True
            self.player.is_invulnerable = True
            self.dash_start_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.player.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time <= self.dash_duration:
                angle_rad = pygame.math.radians(self.player.angle + 90)
                move_vector = pygame.math.Vector2(pygame.math.cos(angle_rad), -pygame.math.sin(angle_rad))
                self.player.pos += move_vector * self.dash_speed
                self.player.rect.center = self.player.pos
            else:
                self.player.is_dashing = False
                self.player.is_invulnerable = False
