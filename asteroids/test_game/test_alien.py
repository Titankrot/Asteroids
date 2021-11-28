import pytest
from asteroids import alien, screen
from asteroids.vector import Vector, Circle
from asteroids.player import Player
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
pygame.display.set_mode((1, 1))


def test_update():
    player = Player(Vector(0, 0), 0, 0, 0, 0)
    enemy = alien.Alien(Vector(1000, 1000), speed=1)
    enemy.update([], player)
    assert Vector(1000, 1000) + (Vector(0, 0) - Vector(1000, 1000))\
        .normalized == enemy.position


def test_draw():
    with patch.object(Circle, 'draw', return_value="None") as mock_draw:
        ammo = alien.Alien(Vector(0, 0))
        mock_window = Mock()
        ammo.draw(mock_window)
    mock_draw.assert_called_once_with(mock_window, pygame.Color("#008000"))
