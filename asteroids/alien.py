from .vector import Vector, Circle
from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME
ALIENS_IMAGE = ""


class Alien:
    def __init__(self, start_position, speed=4):
        self.direction = Vector(1, 0)
        self.position = start_position
        self._speed = speed
        self._max_speed = speed
        # self._normal_image = pygame.image.load(ALIENS_IMAGE)
        # self._rect = self.image.get_rect()
        self.circle = Circle(20, self.position)
        self._radar_radius = 200
        self.bullet_allow = 0

    def update(self, asteroids, player):
        way_to_player = player.position - self.position
        way = Vector(0, 0)
        for asteroid in asteroids:
            way_to_asteroid = asteroid.position - self.position
            if way_to_asteroid.get_length() < self._radar_radius:
                way += -way_to_asteroid
        if way_to_player\
                .get_length() > self._radar_radius:
            way += way_to_player
            self._speed = self._max_speed
        elif way_to_player\
                .get_length() < self._radar_radius // 2:
            way_to_player += -way_to_player
            self._speed = self._max_speed
        else:
            self._speed = 1
        self.direction = way.normalized
        self.position += self.direction * self._speed

    def draw(self, window):
        self.circle.draw(window, pygame.Color("#008000"))
