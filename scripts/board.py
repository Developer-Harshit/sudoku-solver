import pygame

from scripts.util import Vector, generate_text
from scripts.constants import GRAY, WHITE, CYAN, YELLOW

text = generate_text(["", 1, 2, 3, 4, 5, 6, 7, 8, 9])


class Cell:
    def __init__(self, x, y, value=0):
        self.x = x
        self.y = y

        self.value = value
        self.chosen = []

    def render(self, surf, size, offset, color=WHITE):
        width = 0.5
        x = self.x * size + offset.x + self.x // 3 * width * 4
        y = self.y * size + offset.y + self.y // 3 * width * 4

        pygame.draw.rect(
            surf,
            color,
            (x + width / 2, y + width / 2, size - width, size - width),
        )
        fSize = text[self.value].get_size()

        surf.blit(text[self.value], (x + size / 2, y + size / 2))


class Board:
    def __init__(self, dim):
        self.cells = []
        self.size = dim / 11
        self.offset = Vector(self.size, self.size)
        self.size = int(self.size)

        # Creating cells
        for j in range(9):
            self.cells.append([])
            for i in range(9):
                self.cells[j].append(Cell(i, j))

    def returnColliding(self, mpos):
        x = int((mpos[0] - self.offset.x) / self.size)
        y = int((mpos[1] - self.offset.y) / self.size)

        x = min(8, x)
        y = min(8, y)
        x = max(0, x)
        y = max(0, y)

        return Vector(x, y)

    def render_one(self, surf, cell, color=YELLOW):
        cell.render(surf, self.size, self.offset, color)

    def render_many(self, surf, cells, color=CYAN):
        for cell in cells:
            self.render_one(surf, cell, color)

    def render(self, surf, color=WHITE):
        for j in range(9):
            for i in range(9):
                cell = self.cells[j][i]
                if cell.value == 0:
                    cell.render(surf, self.size, self.offset, GRAY)
                else:
                    cell.render(surf, self.size, self.offset, color)
