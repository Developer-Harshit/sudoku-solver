import pygame
import pygame.gfxdraw
from scripts.util import draw_circle,  load_img
from scripts.consts import (
    BLUE,
    RED,
    WHITE,
    G_CONST,
    DELTA,
    BG_COLOR,
)


class Blob:
    def __init__(self, pos, radius, color=WHITE, isStatic=False, update_x=False):
        """
        What blob has :-
            pos - (x,y)
            radius - float
            color - (r,g,b)
            isStatic - Bool
            update_x - Bool
        """
        self.pos = list(pos)
        self.radius = radius
        self.color = color
     


        self.circle = draw_circle(radius, color)

    def applyForce(self, force=(0, 0)):
        if self.isStatic:
            return

        self.force = (self.force[0] + force[0], self.force[1] + force[1])

  
    def render(self, surf):
        surf.blit(self.circle, (self.pos[0] - self.radius, self.pos[1] - self.radius))
