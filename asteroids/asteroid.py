from .vector import Vector, Circle
from . import screen
from os import path
from asteroids.screen import PYGAME


pygame = PYGAME


class Asteroid:
    def __init__(self, direction, start_position, speed, grade,
                 angle_speed=0, angle=0):
        self.__direction = direction
        self.position = start_position
        self.__speed = speed
        self.grade = grade
        self.__angle = angle
        self.__angle_speed = angle_speed
        self.normal_image =\
            pygame.image.load(
                path.join("images", "Asteroid" + str(grade) + ".png"))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.mass = 10 / (pow(2, grade - 1))
        self.circle = Circle(self.rect.width // 3, self.position)

    def update(self,):
        self.__angle += self.__angle_speed
        self.position += self.__direction * self.__speed
        self.position =\
            screen.recalculate_position(self.position, self.rect)
        self.image = pygame.transform.rotate(self.normal_image, self.__angle)
        # pygame.draw.rect(window, Color("#000000"), self.rect, 2)

    def get_dir(self):
        return self.__direction

    def duplicate(self, attac):
        if self.grade != 3:
            dir_0 = self.__direction + attac
            dir_1 = (dir_0 + self.__direction.rotate(90)).normalized
            dir_2 = (dir_0 + self.__direction.rotate(-90)).normalized
            return [Asteroid(dir_1,
                             self.position.copy(), self.__speed,
                             self.grade + 1),
                    Asteroid(dir_2,
                             self.position.copy(), self.__speed,
                             self.grade + 1)]

    def draw(self, window):
        cords = self.position.get_cords()
        window.blit(self.image,
                    (cords[0] - self.rect.width // 2,
                     cords[1] - self.rect.height // 2))
        # self.circle.draw(window, pygame.Color("#000000"))
