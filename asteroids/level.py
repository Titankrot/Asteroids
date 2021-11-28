from .vector import Vector, Circle
from .player import Player
from collections import deque
from .bullet import Bullet
from .asteroid import Asteroid
from .alien import Alien
from .bonus import Bonus, FUEL, AMMO
from random import randint
import math
from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME


class Level:
    def __init__(self, player, asteroids_cooldown, ufo_cooldown,
                 bullet_cooldown, aliens=deque()):
        self.player = player
        self.asteroids = []
        self.bonuses = []
        self.max_cooldown = asteroids_cooldown
        self.ufo_cooldown = ufo_cooldown
        self.max_ufo_cooldown = ufo_cooldown
        self.asteroids_cooldown = asteroids_cooldown
        self.aliens = aliens
        self.bullets = deque()
        self.bullet_allow = 1
        self.bullet_cooldown = bullet_cooldown
        self.horizontal_input = 0
        self.vertical_input = self.player.brake
        self.run = True
        self.score = 0
        self.score_font = pygame.font.SysFont('arial', 25, 1, 1)

    def spawn_random_asteroid(self):
        dir_x = randint(-100, 100)
        dir_y = randint(-100, 100)
        start_x = randint(0, 1)
        start_y = (1 - start_x) * randint(0, screen.WIN_HEIGHT)
        start_x *= randint(0, screen.WIN_WIDTH)
        self.asteroids.append(
            Asteroid(direction=Vector(dir_x, dir_y).normalized,
                     start_position=Vector(start_x, start_y),
                     speed=randint(1, 5), grade=1))

    def control_keys(self):
        self.horizontal_input = 0
        self.vertical_input = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            self.run = False
        if pressed_keys[pygame.K_w]:
            self.vertical_input += 1
        if pressed_keys[pygame.K_s]:
            self.vertical_input += -1
        if pressed_keys[pygame.K_a]:
            self.horizontal_input += 1
        if pressed_keys[pygame.K_d]:
            self.horizontal_input += -1
        if pressed_keys[pygame.K_SPACE]:
            if self.bullet_allow == 0 and self.player.bullets > 0:
                self.bullets.append(
                    Bullet(self.player.direction.copy(),
                           self.player.position + self.player.direction * 20,
                           "player"))
                self.bullet_allow = self.bullet_cooldown
                self.player.bullets -= 1

    def draw(self, work_window, bg, bg_x):
        work_window.blit(bg, (bg_x, 0))
        for asteroid in self.asteroids:
            asteroid.draw(work_window)
        i = 0
        while i < len(self.bullets):
            self.bullets[i].draw(work_window)
            i += 1
        i = 0
        while i < len(self.aliens):
            self.aliens[i].draw(work_window)
            i += 1
        while i < len(self.bonuses):
            self.bonuses[i].draw(work_window)
            i += 1
        self.player.draw(work_window)
        work_window.blit(
            self.score_font.render(
                str.format("Score:{0}",
                           self.score), False, [0, 128, 0]), (10, 10))
        work_window.blit(
            self.score_font.render(
                str.format("Lives:{0}",
                           self.player.health), False, [255, 0, 0]), (600, 10))
        work_window.blit(
            self.score_font.render(
                str.format("Fuel:{0}",
                           int(self.player.fuel)), False, [0, 128, 0]),
            (10, 540))
        work_window.blit(
            self.score_font.render(
                str.format("Bullets:{0}",
                           self.player.bullets), False, [0, 128, 0]),
            (580, 540))

    def update(self):
        is_player_dead = False
        self.update_cooldowns()
        self.player.update(self.horizontal_input, self.vertical_input)
        is_player_dead = self.update_bonuses(is_player_dead)
        is_player_dead = self.update_bullets(is_player_dead)
        is_player_dead = self.update_asteroids(is_player_dead)
        is_player_dead = self.update_aliens(is_player_dead)
        if is_player_dead:
            self.run = False

    def update_bonuses(self, is_player_dead):
        i = 0
        if (self.player.fuel == 50 or self.player.fuel == 25
                or self.player.fuel == 10):
            self.bonuses.append(Bonus(FUEL, Vector(randint(100, 500),
                                                   randint(100, 300))))
        if (self.player.bullets == 30 or self.player.bullets == 15
            or self.player.bullets == 0) \
                and (len(self.bonuses) == 0 or
                     self.bonuses[len(self.bonuses) - 1].type != AMMO):
            self.bonuses.append(Bonus(AMMO, Vector(randint(100, 500),
                                                   randint(100, 300))))
        while i < len(self.bonuses):
            bonus = self.bonuses[i]
            status = bonus.update(self.player)
            if status:
                self.bonuses.remove(bonus)
                i -= 1
            i += 1
        return is_player_dead

    def update_cooldowns(self):
        if self.asteroids_cooldown != 0:
            self.asteroids_cooldown -= 1
        else:
            self.asteroids_cooldown = self.max_cooldown
            self.spawn_random_asteroid()
        if self.ufo_cooldown != 0:
            self.ufo_cooldown -= 1
        else:
            self.ufo_cooldown = self.max_ufo_cooldown
            self.aliens.append(Alien(start_position=Vector(0, 0)))
        if self.bullet_allow != 0:
            self.bullet_allow -= 1
        self.player.immune_time -= 1

    def update_bullets(self, is_player_dead):
        i = 0
        while i < len(self.bullets):
            bullet = self.bullets[i]
            if not bullet.update():
                self.bullets.popleft()
                i -= 1
            else:
                if bullet.circle.is_collision(self.player.circle):
                    if self.player.immune_time < 0:
                        self.player.health -= 25
                        if self.player.health == 0:
                            is_player_dead = True
                        self.player.immune_time = 5
                    self.bullets.remove(bullet)
                    i -= 1
                else:
                    j = 0
                    while j < len(self.aliens):
                        alien = self.aliens[j]
                        if bullet.circle.is_collision(alien.circle):
                            self.aliens.remove(alien)
                            self.bullets.remove(bullet)
                            if bullet.parent == "player":
                                self.score += 30
                            j -= 1
                            i -= 1
                        j += 1
            i += 1
        return is_player_dead

    def update_asteroids(self, is_player_dead):
        for asteroid in self.asteroids:
            asteroid.update()
            if asteroid.circle.is_collision(self.player.circle):
                if self.player.immune_time < 0:
                    self.player.health -= 25
                    if self.player.health == 0:
                        is_player_dead = True
                    self.player.immune_time = 5
                self.asteroids.remove(asteroid)
                two_asteroids = asteroid.duplicate(self.player.direction)
                if two_asteroids:
                    for item in two_asteroids:
                        self.asteroids.append(item)
            if asteroid in self.asteroids:
                i = 0
                while i < len(self.bullets):
                    bullet = self.bullets[i]
                    is_collision_with_bullet = \
                        asteroid.circle.is_collision(bullet.circle)
                    if is_collision_with_bullet:
                        self.asteroids.remove(asteroid)
                        two_asteroids = asteroid.duplicate(bullet.direction)
                        if two_asteroids:
                            for item in two_asteroids:
                                self.asteroids.append(item)
                        if bullet.parent == "player":
                            self.score += 10 * asteroid.grade
                        self.bullets.remove(bullet)
                        i -= 1
                        break
                    i += 1
            if asteroid in self.asteroids:
                i = 0
                while i < len(self.aliens):
                    alien = self.aliens[i]
                    is_collision_with_alien = \
                        asteroid.circle.is_collision(alien.circle)
                    if is_collision_with_alien:
                        self.asteroids.remove(asteroid)
                        two_asteroids = asteroid.duplicate(alien.direction)
                        if two_asteroids:
                            for item in two_asteroids:
                                self.asteroids.append(item)
                        self.aliens.remove(alien)
                        i -= 1
                    i += 1
        return is_player_dead

    def update_aliens(self, is_player_dead):
        i = 0
        while i < len(self.aliens):
            alien = self.aliens[i]
            alien.update(self.asteroids, self.player)
            if (self.player.position - alien.position) \
                    .get_length() < 200 and alien.bullet_allow <= 0:
                directory = (self.player.position - alien.position).normalized
                self.bullets.append(
                    Bullet(directory,
                           alien.position + directory * 21))
                alien.bullet_allow = 100
            alien.bullet_allow -= 1
            is_collision_with_player = \
                alien.circle.is_collision(self.player.circle)
            if is_collision_with_player:
                if self.player.immune_time < 0:
                    self.player.health -= 25
                    if self.player.health == 0:
                        is_player_dead = True
                    self.player.immune_time = 5
                self.aliens.remove(alien)
                i -= 1
            i += 1
        return is_player_dead
