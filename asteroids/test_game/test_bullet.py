import pytest
from asteroids import bullet, screen
from asteroids.vector import Vector, Circle
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
pygame.display.set_mode((1, 1))


def test_update_lifetime():
    ammo = bullet.Bullet(Vector(0, 0), Vector(0, 0), life_time=1)
    assert ammo.update()
    assert not ammo.update()


def test_update():
    ammo = bullet.Bullet(Vector(1, 2), Vector(0, 0), life_time=-1)
    pos = ammo.circle.center.copy()
    ammo.update()
    assert pos != ammo.circle.center
    offset = ammo.circle.center - pos
    ammo.update()
    assert pos + offset * 2 == ammo.circle.center


def test_draw():
    with patch.object(Circle, 'draw', return_value="None") as mock_draw:
        ammo = bullet.Bullet(Vector(0, 0), Vector(0, 0), life_time=1)
        mock_window = Mock()
        ammo.draw(mock_window)
    mock_draw.assert_called_once_with(mock_window, pygame.Color("#ff0000"))
