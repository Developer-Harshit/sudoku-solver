import pygame


def load_img(rpath):
    path = rpath

    img = pygame.image.load(path).convert()  # convert method makes it easier to render

    img.set_colorkey((0, 0, 0))
    return img


def draw_circle(radius, color=(255, 255, 255)):
    surf = pygame.Surface((radius * 2, radius * 2))

    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

