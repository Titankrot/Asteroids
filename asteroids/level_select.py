from . import level1, level2, level3, screen
from .menu import Menu
from os import path
from asteroids.screen import PYGAME


pygame = PYGAME

BACKGROUND_IMAGE = path.join("images", "Background2.png")
FONT_SIZE = 80
OFFSET = 40
PICKED_COLOR = [0, 128, 0]
NOT_PICKED_COLOR = [255, 255, 255]


def main(work_window, work_lock):
    pygame.font.init()
    level_select = Menu(BACKGROUND_IMAGE,
                        FONT_SIZE,
                        'arial',
                        OFFSET,
                        PICKED_COLOR,
                        NOT_PICKED_COLOR,
                        "level 1", "level 2", "level 3", "back")
    while level_select.run:
        work_lock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                level_select.update(event.key)
        level_select.update(pygame.key.get_pressed())
        level_select.draw(work_window)
        menu_event = level_select.events[level_select.picked_index]
        if not level_select.run:
            if menu_event == "back":
                return True
            if menu_event == "level 1":
                return level1.main(work_window, work_lock)
            if menu_event == "level 2":
                return level2.main(work_window, work_lock)
            if menu_event == "level 3":
                return level3.main(work_window, work_lock)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return False


if __name__ == "__main__":
    pass
