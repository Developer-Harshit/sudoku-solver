import pygame
import pygame.gfxdraw
from scripts.constants import BLACK, ORANGE


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Mouse:
    def __init__(self):
        self.pos = (0, 0)

        self.circle = draw_circle(8, ORANGE)

    def render(self, surf):
        surf.blit(self.circle, (self.pos[0] - 8, self.pos[1] - 8))


def draw_circle(radius, color=(255, 255, 255)):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def generate_text(txt_list, fontsize=32):
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.Font("mono.ttf", fontsize)
    text = []

    for txt in txt_list:
        text.append(font.render(str(txt), True, BLACK))
    return text


msg = generate_text(
    [
        "click 'S' to start",
        "Running Sudoku solver",
        "finished",
        "no solutions,board might be invalid",
        "type any number from 0 to 9 to edit the board",
        "click 'Q' to quit,click 'R' to restart",
    ],
    16,
)
