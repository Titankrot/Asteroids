import pytest
from asteroids import screen
from asteroids.vector import Vector, Circle
from asteroids.asteroid import Asteroid
from os import path
from mock import Mock, patch, MagicMock
from asteroids.screen import PYGAME


pygame = PYGAME
VECTORZERO = Vector(0, 0)
VECTORONE = Vector(1, 1)

pygame.init()
pygame.display.set_mode((1, 1))


def test_draw():
    def blit():
        pass
    mock_window = Mock()
    mock_window.take(blit)
    Asteroid(VECTORZERO, VECTORZERO, 0, 1).draw(mock_window)
    assert 1 == mock_window.blit.call_count


def test_duplicate():
    a = Asteroid(VECTORZERO, VECTORZERO, 0, 3)
    assert a.duplicate(VECTORZERO) is None
    a = Asteroid(VECTORONE, VECTORZERO, 0, 1)
    asteroids = a.duplicate(-VECTORONE)
    first = asteroids[0]
    second = asteroids[1]
    assert first != second
    assert second.get_dir() != first.get_dir()
    assert a.position == first.position == second.position
    assert 2 == first.grade == second.grade


def test_update():
    a = Asteroid(VECTORONE, VECTORZERO, 1, 3)
    a.update()
    assert VECTORONE * 1 == a.position
