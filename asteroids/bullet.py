from .vector import Vector, Circle
from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME


class Bullet:
    def __init__(self, direction, start_position, parent="UFO", life_time=40,
                 speed=10):
        self.direction = direction.normalized
        self.__position = start_position
        self.__speed = speed
        self.__life_time = life_time
        self.rect = pygame.Rect(start_position.x, start_position.y, 5, 5)
        self.mass = 1
        self.circle = Circle(self.rect.width, self.__position)
        self.parent = parent

    def update(self):
        if self.__life_time == 0:
            return False
        self.__life_time -= 1
        self.__position += self.direction * self.__speed
        self.__position =\
            screen.recalculate_position(self.__position, self.rect)
        return True

    def draw(self, window):
        self.circle.draw(window, pygame.  Color("#ff0000"))
