import math
from asteroids.screen import PYGAME


pygame = PYGAME


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __str__(self):
        return "{0} {1}".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        return self

    def get_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    def get_cords(self):
        return int(self.x), int(self.y)

    def rotate(self, angle):
        x = self.x
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = x * math.sin(angle) + self.y * math.cos(angle)
        return Vector(self.x, self.y)

    @property
    def normalized(self):
        return Vector(self.x / self.get_length(),
                      self.y / self.get_length())\
            if self.get_length() > 0 else Vector(0, 0)

    def normalize(self):
        self.x = self.x / self.get_length()
        self.y = self.y / self.get_length()

    def copy(self):
        return Vector(self.x, self.y)


class Circle:
    def __init__(self, radius, center: Vector):
        self.radius = radius
        self.center = center

    def is_collision(self, another):
        return self.radius + another.radius >= \
               (self.center - another.center).get_length()

    def draw(self, window: pygame.Surface, color):
        pygame.draw.circle(window, color, self.center.get_cords(), self.radius)


if __name__ == '__main__':
    pass
