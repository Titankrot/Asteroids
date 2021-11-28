import pytest
from asteroids import player, screen
from asteroids.vector import Vector
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
pygame.display.set_mode((1, 1))
PLAYER = player.Player(Vector(0, 0), 1, 1, 1, 1)


def test_update():
    start_pos = PLAYER.position.copy()
    PLAYER.update(1, 1)
    assert start_pos != PLAYER.position


def test_draw():
    def blit():
        pass
    mock_window = Mock()
    mock_window.take(blit)
    PLAYER.draw(mock_window)
    assert 1 == mock_window.blit.call_count
