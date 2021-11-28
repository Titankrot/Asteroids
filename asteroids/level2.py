from .vector import Vector
from .player import Player
from collections import deque
from .bullet import Bullet
from .asteroid import Asteroid
from .level import Level
from .alien import Alien
from .scoreboard import ScoreTable
from random import randint
import math
from os import path
from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME
BACKGROUND_IMAGE = path.join(".", "images", "Background2.png")
FILENAME = path.join("level2data.dat")


def main(work_window, work_clock):
    bg = pygame.image.load(BACKGROUND_IMAGE)
    player = Player(position=Vector(300, 200),
                    acceleration=0.5,
                    angular_acceleration=0.5,
                    max_speed=5,
                    max_angular_speed=5)
    alien = Alien(start_position=Vector(0, 0))
    aliens = deque()
    aliens.append(alien)
    level = Level(player,
                  ufo_cooldown=200,
                  asteroids_cooldown=-1,
                  bullet_cooldown=10,
                  aliens=aliens)
    while level.run:
        work_clock.tick(screen.FPS)
        level.control_keys()
        level.update()
        level.draw(work_window, bg, 0)
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return False
    score_table = ScoreTable(FILENAME, level.score)
    while score_table.is_work:
        work_clock.tick(screen.FPS)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return False
            elif i.type == pygame.KEYDOWN:
                score_table.update(i.key)
        score_table.draw(work_window, bg, 0)
    return True


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((screen.WIN_WIDTH, screen.WIN_HEIGHT))
    clock = pygame.time.Clock()
    main(window, clock)
