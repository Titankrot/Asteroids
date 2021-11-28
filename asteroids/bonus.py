from .vector import Vector, Circle
from .player import Player
from asteroids.screen import PYGAME


pygame = PYGAME
AMMO = "#7b3f00"
FUEL = "#d5265b"
DELTATTL = 0.1


class Bonus:
    def __init__(self, bonus_type, pos):
        self.type = bonus_type
        self.ttl = 20
        self.radius = 10
        self.pos = pos
        self.circle = Circle(self.radius, self.pos)

    def update(self, player):
        self.ttl -= DELTATTL
        if self.circle.is_collision(player.circle):
            if self.type == AMMO:
                player.bullets = 100
            if self.type == FUEL:
                player.fuel = 100
        elif self.ttl > 0:
            return False
        return True

    def draw(self, window):
        self.circle.draw(window, pygame.Color(self.type))
