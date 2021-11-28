from asteroids.vector import Vector, Circle
import random
import pytest
import math


ZERO_VECTOR = Vector(0, 0)
ONE_VECTOR = Vector(1, 1)
RANDOM_VECTOR1 = Vector(random.random(), random.random())
RANDOM_VECTOR2 = Vector(random.random(), random.random())
X = random.random()
Y = random.random()


class TestVector:
    def test_eq(self):
        assert Vector(X, Y) == Vector(X, Y)

    def test_str(self):
        assert str(Vector(X, Y)) == str.format("{0} {1}", X, Y)
        assert Vector(X, Y).__repr__() == str.format("{0} {1}", X, Y)

    def test_sum_with_zero(self):
        assert ZERO_VECTOR + RANDOM_VECTOR1 == RANDOM_VECTOR1

    def test_sum_with_two_vectors(self):
        vector = RANDOM_VECTOR1 + RANDOM_VECTOR2
        assert vector == RANDOM_VECTOR2 + RANDOM_VECTOR1

    def test_bad_sum(self):
        assert ZERO_VECTOR != ONE_VECTOR

    def test_sum_on_natural(self):
        assert Vector(0, 1) + Vector(1, 0) == ONE_VECTOR

    def test_minus(self):
        assert ONE_VECTOR == -Vector(-1, -1)

    def test_mul(self):
        i = random.random()
        assert Vector(X, Y) * i == Vector(X * i, Y * i)

    def test_sub(self):
        assert ONE_VECTOR - ONE_VECTOR == ZERO_VECTOR

    def test_rmul(self):
        i = random.random()
        assert i * Vector(X, Y) == Vector(X * i, Y * i)

    def test_truediv(self):
        i = random.random() + 1
        assert Vector(X, Y) / i == Vector(X / i, Y / i)

    def test_get_length(self):
        assert Vector(X, Y).get_length() == math.sqrt(X ** 2 + Y ** 2)

    def test_get_angle(self):
        assert Vector(X, Y).get_angle() == math.degrees(math.atan2(Y, X))

    def test_get_cords(self):
        assert Vector(X, Y).get_cords() == (int(X), int(Y))

    def test_rotate(self):
        vector = Vector(X, Y)
        i = random.randrange(0, 360)
        vector = vector.rotate(i)
        vector2 = Vector(X * math.cos(i) - Y * math.sin(i),
                         X * math.sin(i) + Y * math.cos(i))
        assert vector == vector2

    def test_normalized(self):
        assert Vector(0, 20).normalized == Vector(0, 1)

    def test_normalize(self):
        vector = Vector(30, 0)
        vector.normalize()
        assert vector == Vector(1, 0)

    def test_copy(self):
        vector = Vector(X, Y)
        vector2 = vector.copy()
        vector += Vector(Y, X)
        assert vector != vector2


class TestCircle:
    def test_collision_centre(self):
        i = random.random()
        assert Circle(i, ZERO_VECTOR).is_collision(Circle(i*i, ZERO_VECTOR))

    def test_collision_random(self):
        i = random.randrange(0, 100)
        x = random.randrange(0, 2 * i) - i
        y = random.randrange(0, 2 * i) - i
        assert Circle(i, Vector(X, Y)).is_collision(
            Circle(i, Vector(X + x, Y + y)))

    def test_not_collision(self):
        i = random.random()
        assert Circle(i, Vector(X, Y)).is_collision(
            Circle(i, Vector(X + i * i, Y + i * i)))
