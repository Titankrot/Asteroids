import pytest
from asteroids import menu
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
BACKGROUND_IMAGE = path.join("images", "Background2.png")
MENU = menu.Menu(BACKGROUND_IMAGE,
                 1,
                 "Arial",
                 1,
                 [0, 128, 0],
                 [255, 255, 255],
                 "first",
                 "second",
                 "third")


def test_update():
    pressed_keys = 119
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 0
    pressed_keys = 115
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 1
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 2
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 2
    pressed_keys = 119
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 1
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert MENU.picked_index == 0
    pressed_keys = 13
    MENU.timer = 0
    MENU.update(pressed_keys)
    assert not MENU.run


def test_draw():
    def blit():
        pass
    mock_window = Mock()
    mock_window.take(blit)
    pygame.display.set_mode((1, 1))
    MENU.draw(mock_window)
    assert 4 == mock_window.blit.call_count
