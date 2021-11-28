import pygame
from pygame import *
from asteroids import level_select
from asteroids.menu import Menu
from os import path
import sys
from asteroids import screen


sys.path.insert(0, path.join("Asteroids"))
BACKGROUND_IMAGE = path.join("images", "Background2.png")
FONT_SIZE = 80
OFFSET = 40
PICKED_COLOR = [0, 128, 0]
NOT_PICKED_COLOR = [255, 255, 255]


def main():
    font.init()
    main_menu = Menu(BACKGROUND_IMAGE,
                     FONT_SIZE,
                     'arial',
                     OFFSET,
                     PICKED_COLOR,
                     NOT_PICKED_COLOR,
                     "Start", "Exit")
    while main_menu.run:
        clock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main_menu.update(event.key)
        main_menu.draw(window)
        menu_event = main_menu.events[main_menu.picked_index]
        if not main_menu.run:
            if menu_event != "Exit":
                main_menu.run = True
            if menu_event == "Start":
                if not level_select.main(window, clock):
                    main_menu.run = False
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                main_menu.run = False
                break
    font.quit()
    pygame.quit()


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "--tracing":
            screen.RAY_TRACING = True
    pygame.init()
    window = pygame.display.set_mode((screen.WIN_WIDTH, screen.WIN_HEIGHT))
    clock = pygame.time.Clock()
    main()
