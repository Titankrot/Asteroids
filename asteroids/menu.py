from . import screen
from asteroids.screen import PYGAME


pygame = PYGAME


class Menu:
    def __init__(self,
                 background,
                 font_size, typeface, offset,
                 picked_color, not_picked_color,
                 *events):
        self.bg = pygame.image.load(background)
        self.offset = offset
        self.picked_color = picked_color
        self.not_picked_color = not_picked_color
        self.font_size = font_size
        menu_font = pygame.font.SysFont(typeface, self.font_size)
        menu_picked_font = pygame.font.SysFont(typeface, font_size + 5)
        self.picked_index = 0
        self.events = events
        self.bottoms = \
            [menu_font.render(i, False, self.not_picked_color)
             for i in self.events]
        self.bottoms_picked =\
            [menu_picked_font.render(i, False, self.picked_color)
             for i in self.events]
        self.run = True
        self.timer = 3

    def draw(self, window):
        window.blit(self.bg, (0, 0))
        for i in range(0, len(self.bottoms)):
            window.blit(self.bottoms[i]
                        if self.picked_index != i
                        else self.bottoms_picked[i],
                        (self.offset, self.offset + self.font_size * i))
        pygame.display.update()

    def update(self, pressed_key):
        if pressed_key == pygame.K_w and self.picked_index != 0:
            self.picked_index -= 1
        if pressed_key == pygame.K_s \
                and self.picked_index != len(self.bottoms)-1:
            self.picked_index += 1
        if pressed_key == pygame.K_RETURN:
            self.run = False
