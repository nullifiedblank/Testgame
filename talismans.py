import pygame

class Talisman:
    def __init__(self, name):
        self.name = name

    def update(self, player):
        pass

    def on_deal_damage(self, player, target, damage_source_has_slow=False):
        pass

    def on_take_damage(self, player, damage_amount):
        pass

class FrostAmulet(Talisman):
    def __init__(self):
        super().__init__("Frost Amulet")

    def on_deal_damage(self, player, target, damage_source_has_slow=False):
        if hasattr(target, 'apply_slow'):
            if damage_source_has_slow:
                target.apply_slow(strength=0.6, duration=600)
            else:
                target.apply_slow(strength=0.8, duration=600)

class TalismanOfRejuvenation(Talisman):
    def __init__(self):
        super().__init__("Talisman of Rejuvenation")

    def update(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - player.last_damage_time > 3000 and player.last_damage_value > 0:
            heal_amount = player.last_damage_value + 15
            player.health.heal(heal_amount)
            player.last_damage_value = 0 # Reset after healing

TALISMANS = {
    "frost_amulet": FrostAmulet(),
    "talisman_of_rejuvenation": TalismanOfRejuvenation()
}
