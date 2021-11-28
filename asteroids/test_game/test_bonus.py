import pytest
from asteroids import screen
from asteroids.vector import Vector, Circle
from asteroids.bonus import *
from os import path
from mock import Mock, patch, MagicMock
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
pygame.display.set_mode((1, 1))


def test_draw():
    with patch.object(Circle, 'draw', return_value="None") as mock_draw:
        ammo1 = Bonus(AMMO, Vector(0, 0))
        mock_window = Mock()
        ammo1.draw(mock_window)
        mock_draw.assert_called_once_with(mock_window, pygame.Color(AMMO))
    with patch.object(Circle, 'draw', return_value="None") as mock_draw:
        ammo2 = Bonus(FUEL, Vector(0, 0))
        mock_window = Mock()
        ammo2.draw(mock_window)
        mock_draw.assert_called_once_with(mock_window, pygame.Color(FUEL))


def test_update():
    bonus = Bonus(AMMO, Vector(0, 0))
    ttl = bonus.ttl
    assert not bonus.update(Player(Vector(100, 100), 0, 0, 0, 0))
    assert ttl - DELTATTL == bonus.ttl
    assert bonus.update(Player(Vector(0, 0), 0, 0, 0, 0))
    for i in range(int(bonus.ttl / DELTATTL)):
        bonus.update(Player(Vector(100, 100), 0, 0, 0, 0))
    assert bonus.update(Player(Vector(100, 100), 0, 0, 0, 0))
