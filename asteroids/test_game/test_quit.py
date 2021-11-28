import pytest
from asteroids import menu, level_select, level1, level2, level3
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.vector import *
from asteroids.screen import PYGAME


pygame = PYGAME
WL = Mock()
WW = Mock()
EVENT = Mock()
EVENT.type = pygame.QUIT


def test_level_select():
    pygame.init()
    with patch.object(pygame.event, "get", return_value=[EVENT]):
        assert not level_select.main(WW, WL)


def test_level1():
    pygame.init()
    with patch.object(pygame.event, "get", return_value=[EVENT]):
        assert not level1.main(WW, WL)


def test_level2():
    pygame.init()
    with patch.object(pygame.event, "get", return_value=[EVENT]):
        with patch.object(Circle, 'draw', return_value="None"):
            assert not level2.main(WW, WL)


def test_level3():
    pygame.init()
    with patch.object(pygame.event, "get", return_value=[EVENT]):
        with patch.object(Circle, 'draw', return_value="None"):
            assert not level3.main(WW, WL)
