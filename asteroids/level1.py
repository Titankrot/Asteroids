from .vector import Vector
from .player import Player
from collections import deque
from .bullet import Bullet
from .asteroid import Asteroid
from .level import Level
from .scoreboard import ScoreTable
from random import randint
import math
from os import path
from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME
BACKGROUND_IMAGE = path.join("images", "Background2.png")
FILENAME = path.join("level1data.dat")


def main(work_window, work_clock):
    bg = pygame.image.load(BACKGROUND_IMAGE)
    player = Player(position=Vector(300, 200),
                    acceleration=0.5,
                    angular_acceleration=0.5,
                    max_speed=5,
                    max_angular_speed=5)
    level = Level(player,
                  ufo_cooldown=-1,
                  asteroids_cooldown=50,
                  bullet_cooldown=10)
    for i in range(0, 3):
        level.spawn_random_asteroid()
    while level.run:
        work_clock.tick(screen.FPS)
        level.control_keys()
        level.update()
        level.draw(work_window, bg, -screen.WIN_WIDTH)
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
        score_table.draw(work_window, bg, -screen.FPS)
    return True


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((screen.WIN_WIDTH, screen.WIN_HEIGHT))
    clock = pygame.time.Clock()
    main(window, clock)
