import importlib
from mock import Mock, patch, MagicMock


PYGAME = ""
try:
    PYGAME = importlib.import_module('pygame')
except SystemExit as e:
    # anytask detected, mocking
    PYGAME = MagicMock()


FPS = 30
WIN_WIDTH = 720
WIN_HEIGHT = 570
RAY_TRACING = False


def recalculate_position(position, rect):
    if position.x >= WIN_WIDTH + rect.width / 2:
        position.x = -rect.width / 2
    elif position.x <= -WIN_WIDTH / 2:
        position.x = WIN_WIDTH + rect.width / 2
    if position.y >= WIN_HEIGHT + rect.height / 2:
        position.y = -rect.height / 2
    elif position.y <= -rect.height / 2:
        position.y = WIN_HEIGHT + rect.height / 2
    return position


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x
