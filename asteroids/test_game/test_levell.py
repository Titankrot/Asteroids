import pytest
from asteroids.level import Level
from asteroids import player, bonus, bullet, alien, asteroid
from asteroids.vector import *
from os import path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME
pygame.init()
pygame.display.set_mode((1, 1))
PLAYER = player.Player(Vector(0, 0), 1, 1, 1, 1)
LEVEL = Level(PLAYER, 1, 1, 1)
KEYS = {pygame.K_ESCAPE: False,
        pygame.K_w: False,
        pygame.K_s: False,
        pygame.K_a: False,
        pygame.K_d: False,
        pygame.K_SPACE: False}
VECTORZERO = Vector(0, 0)
VECTORBIG = Vector(1000, 1000)


def test_spawn_random_asteroid():
    LEVEL.spawn_random_asteroid()
    assert 1 == len(LEVEL.asteroids)


def test_control_keys():
    with patch.object(pygame.key, "get_pressed", return_value=KEYS):
        LEVEL.control_keys()
        assert LEVEL.run
        KEYS[pygame.K_ESCAPE] = True
        LEVEL.control_keys()
        assert not LEVEL.run
        assert 0 == LEVEL.vertical_input
        KEYS[pygame.K_w] = True
        LEVEL.control_keys()
        assert 1 == LEVEL.vertical_input
        KEYS[pygame.K_s] = True
        LEVEL.control_keys()
        assert 0 == LEVEL.vertical_input
        assert 0 == LEVEL.horizontal_input
        KEYS[pygame.K_a] = True
        LEVEL.control_keys()
        assert 1 == LEVEL.horizontal_input
        KEYS[pygame.K_d] = True
        LEVEL.control_keys()
        assert 0 == LEVEL.horizontal_input
        KEYS[pygame.K_SPACE] = True
        LEVEL.control_keys()
        assert 0 == len(LEVEL.bullets)
        LEVEL.bullet_allow = 0
        LEVEL.control_keys()
        assert 1 == len(LEVEL.bullets)


def test_draw():
    def blit():
        pass
    mock_window = Mock()
    mock_window.take(blit)
    with patch.object(Circle, 'draw', return_value="None") as mock_draw:
        LEVEL.draw(mock_window, " ", 0)
    assert 0 != mock_window.blit.call_count
    assert 0 != mock_draw.call_count


def test_update():
    level = Level(PLAYER, 1, 1, 1)
    level.update()
    assert level.run
    level = Level(PLAYER, 1, 1, 1)
    with patch.object(Level, "update_bullets", return_value=True):
        level.update()
        assert not level.run
    level = Level(PLAYER, 1, 1, 1)
    with patch.object(Level, "update_asteroids", return_value=True):
        level.update()
        assert not level.run
    level = Level(PLAYER, 1, 1, 1)
    with patch.object(Level, "update_aliens", return_value=True):
        level.update()
        assert not level.run


def test_update_bonuses():
    level = Level(PLAYER, 1, 1, 1)
    level.update_bonuses(False)
    assert 0 == len(level.bonuses)
    level.player.fuel = 50
    level.player.bullets = 30
    level.update_bonuses(False)
    assert 2 == len(level.bonuses)
    level.player.fuel = 100
    level.player.bullets = 100
    with patch.object(bonus.Bonus, "update", return_value=True):
        level.update_bonuses(False)
    assert 0 == len(level.bonuses)


def test_update_cooldowns():
    level = Level(PLAYER, 1, 1, 1)
    level.asteroids_cooldown = 1
    level.ufo_cooldown = 1
    level.bullet_allow = 1
    level.update_cooldowns()
    assert 0 == len(level.asteroids)
    assert 0 == len(level.aliens)
    assert 0 == level.bullet_allow
    level.asteroids_cooldown = 0
    level.ufo_cooldown = 0
    level.bullet_allow = 0
    level.update_cooldowns()
    assert 1 == len(level.asteroids)
    assert 1 == len(level.aliens)
    assert 0 == level.bullet_allow


def test_update_bullets():
    level = Level(PLAYER, 1, 1, 1)
    level.player.immune_time = -1
    level.player.health = 25
    level.bullets.append(bullet.Bullet(VECTORZERO, VECTORZERO, speed=0))
    assert level.update_bullets(False)
    level = Level(PLAYER, 1, 1, 1)
    level.bullets.append(bullet.Bullet(VECTORBIG, VECTORBIG, speed=0))
    level.aliens.append(alien.Alien(VECTORBIG))
    assert not level.update_bullets(False)
    assert 2 == len(level.aliens)
    assert 0 == len(level.bullets)


def test_update_asteroids():
    level = Level(PLAYER, 1, 1, 1)
    level.spawn_random_asteroid()
    level.bullets.append(bullet.Bullet(VECTORZERO, VECTORZERO, speed=0))
    level.aliens.append(alien.Alien(VECTORBIG))
    assert level.update_asteroids(True)


def test_update_aliens():
    level = Level(PLAYER, 1, 1, 1)
    level.aliens.append(alien.Alien(VECTORZERO))
    assert level.update_aliens(True)
