import pygame

class Health:
    def __init__(self, owner, max_hp):
        self.owner = owner # The sprite this component is attached to
        self.max_hp = max_hp
        self.current_hp = max_hp

    def take_damage(self, amount):
        if amount < 0: return

        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0
            self.die()

    def heal(self, amount):
        if amount < 0: return
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def die(self):
        # When health reaches zero, tell the owner sprite to kill itself
        self.owner.kill()
