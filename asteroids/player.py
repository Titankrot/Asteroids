from .vector import Vector, Circle
from . import screen
from os import path
from asteroids.screen import PYGAME


pygame = PYGAME
PLAYER_IMAGE = path.join("images", "player.png")


class Player:
    def __init__(self,
                 position,
                 acceleration,
                 angular_acceleration,
                 max_speed,
                 max_angular_speed):
        self.speed = 0
        self.fuel = 100
        self.bullets = 50
        self._max_speed = max_speed
        self._acceleration = acceleration
        self.position = position.copy()
        self.direction = Vector(0, -1)
        self.move_direction = self.direction.copy()
        self.movement = Vector(0, 0)
        self.angular_speed = 0
        self._max_angular_speed = max_angular_speed
        self._angular_acceleration = angular_acceleration
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self._rotated_image = self.image
        self.rect = self.image.get_rect(center=(position.x, position.y))
        self.brake = -0.1
        self.health = 100
        self.immune_time = 5
        self.mass = 1
        self.circle = Circle(self.rect.width // 2, self.position)

    def update(self, horizontal, vertical):
        if self.fuel <= 0:
            horizontal = 0
            vertical = 0
        if vertical != 0:
            self.fuel -= 0.5
        self.speed += self._acceleration * vertical
        self.speed = min(self.speed, self._max_speed)
        self.speed = max(self.speed, 0)
        if horizontal == 0:
            self.angular_speed = 0
        else:
            if screen.sign(self.angular_speed) != screen.sign(horizontal):
                self.angular_speed = 0
            self.angular_speed -= self._angular_acceleration * horizontal
            self.angular_speed =\
                min(self.angular_speed, self._max_angular_speed)
            self.angular_speed =\
                max(self.angular_speed, -self._max_angular_speed)
            self.direction =\
                (self.direction.rotate(self.angular_speed / 10) * 100)\
                .normalized
        if vertical > 0:
            self.move_direction += \
                self.direction.normalized * self._acceleration
        move_length = self.move_direction.get_length() + self.brake
        move_length = min(self.speed, move_length)
        move_length = max(0, move_length)
        self.move_direction = self.move_direction.normalized * move_length
        self.position += self.move_direction
        self.position =\
            screen.recalculate_position(self.position, self.rect)
        self._rotated_image =\
            pygame.transform.rotate(self.image, -self.direction.get_angle())
        self.rect = self._rotated_image.get_rect(
            center=(self.position.x, self.position.y))

    def draw(self, window):
        # cords = self.position.get_cords()
        # window.blit(self._rotated_image,
        #             (cords[0] - self.rect.width // 2,
        #              cords[1] - self.rect.height // 2))
        window.blit(self._rotated_image, self.rect)
        if screen.RAY_TRACING:
            pygame.draw.line(window, Color("#ff0000"),
                             (self.position.x, self.position.y),
                             (self.position.x + self.move_direction.x * 20,
                              self.position.y + self.move_direction.y * 20))
            pygame.draw.line(window, Color("#0000ff"),
                             (self.position.x, self.position.y),
                             (self.position.x + self.direction.x * 20,
                              self.position.y + self.direction.y * 20))

        # self.circle.draw(window, Color("#000000"))
        # pygame.draw.rect(window, Color("#000000"), self.rect, 2)
