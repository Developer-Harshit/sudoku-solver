import sys
import pygame
import pygame.gfxdraw
from random import random, randint


print("Initializing")

DIM = 800
SPEED = 1
SEP1 = 1
SEP2 = 5
GRAY = "#764f51"
CYAN = "#9AD0BE"
WHITE = "#F7F5B2"
BLACK = "#171617"
YELLOW = "#F0A830"
ORANGE = "#F07818"
BG_COLOR = "#DAD5BA"


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def generate_text(txt_list, fonsize=32, color=BLACK):
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.Font("mono.ttf", fonsize)
    text = []

    for txt in txt_list:
        text.append(font.render(str(txt), True, color))
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

text = generate_text(["", 1, 2, 3, 4, 5, 6, 7, 8, 9])


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Mouse:
    def __init__(self):
        self.pos = (0, 0)
        self.circle = pygame.Surface((16, 16))
        pygame.draw.circle(self.circle, ORANGE, (8, 8), 8)
        self.circle.set_colorkey((0, 0, 0))

    def render(self, surf):
        surf.blit(self.circle, (self.pos[0] - 8, self.pos[1] - 8))


class Solver:
    def __init__(self, program):
        self.cells = program.board.cells
        self.program = program
        self.closedset = []

    def getEmpty(self):
        for j in range(9):
            for i in range(9):
                cell = self.cells[j][i]
                if cell.value == 0:
                    return cell
        return False

    def valid_rows(self, cell, result):
        x = cell.x
        y = cell.y

        for i in range(9):
            if x == i:
                continue
            other = self.cells[y][i]
            if other.value in result:
                result.remove(other.value)

    def valid_cols(self, cell, result):
        x = cell.x
        y = cell.y

        for j in range(9):
            if y == j:
                continue
            other = self.cells[j][x]
            if other.value in result:
                result.remove(other.value)

    def valid_subgrid(self, cell, result):
        x = cell.x
        y = cell.y
        startRow = x - x % 3
        startCol = y - y % 3

        for j in range(startCol, startCol + 3):
            for i in range(startRow, startRow + 3):
                if x == i and y == j:
                    continue
                other = self.cells[j][i]
                if other.value in result:
                    result.remove(other.value)

    def backtrack(self, curr):
        if not self.closedset:
            self.program.state = 3
            return
        curr.chosen = []
        prev = self.closedset.pop()
        self.program.current = prev
        prev.value = 0

    def solve(self):
        if self.program.state in [0, 2, 3]:
            return
        curr = self.getEmpty()
        if not curr:
            self.program.state = 2
            return
        self.program.current = curr

        values = []
        for i in range(1, 10):
            if i not in curr.chosen:
                values.append(i)
        self.valid_rows(curr, values)
        self.valid_cols(curr, values)
        self.valid_subgrid(curr, values)

        if not values:
            return self.backtrack(curr)

        curr.value = values[randint(0, len(values) - 1)]
        curr.chosen.append(curr.value)
        self.closedset.append(curr)


class Cell:
    def __init__(self, x, y, value=0):
        self.x = x
        self.y = y

        self.value = value
        self.chosen = []

    def render(self, surf, size, offset, color=WHITE):
        x = self.x * size + offset.x + self.x // 3 * SEP2
        y = self.y * size + offset.y + self.y // 3 * SEP2

        pygame.draw.rect(
            surf,
            color,
            (x + SEP1 / 2, y + SEP1 / 2, size - SEP1, size - SEP1),
        )
        fSize = text[self.value].get_size()

        surf.blit(text[self.value], (x + size / 2, y + size / 2))


class Board:
    def __init__(self):
        self.cells = []
        self.size = DIM / 11
        self.offset = Vector(self.size, self.size)
        self.size = int(self.size)

        for j in range(9):
            self.cells.append([])
            for i in range(9):
                self.cells[j].append(Cell(i, j))

    def getCords(self, mpos):
        x = int((mpos[0] - self.offset.x) / self.size)
        y = int((mpos[1] - self.offset.y) / self.size)

        return Vector(clamp(x, 0, 8), clamp(y, 0, 8))

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


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")

        self.screen = pygame.display.set_mode((DIM, DIM), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        self.mouse = Mouse()
        self.restart()
        self.current = self.board.cells[0][0]

    def restart(self):
        self.board = Board()
        self.solver = Solver(self)
        self.state = 0

    def render_text(self, offset):
        txt = msg[self.state]

        size = txt.get_size()
        self.screen.blit(
            txt, ((DIM / 2 - size[0] / 2, DIM + size[1] / 2 - offset), size)
        )
        vstate = min(self.state + 4, 5)
        txt = msg[vstate]
        size = txt.get_size()

        self.screen.blit(txt, ((DIM / 2 - size[0] / 2, offset + size[1] / 2), size))

    def quit(self):
        print("Exiting")
        pygame.quit()
        sys.exit()

    def run(self):
        frame = 0
        fontoffset = self.board.size / 2
        while True:
            frame += 1
            mpos = pygame.mouse.get_pos()
            self.mouse.pos = list(mpos)
            if self.state == 0:
                bpos = self.board.getCords(mpos)
                self.current = self.board.cells[bpos.y][bpos.x]

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quit()
                        break
                    if event.key == pygame.K_r:
                        print("Restarting")
                        self.restart()

                    if event.key == pygame.K_s and self.state == 0:
                        print("Starting")
                        self.state = 1

                    digit = event.key - 48
                    if self.state == 0 and digit > -1 and digit < 10:
                        self.current.value = digit

                if event.type == pygame.QUIT:
                    self.quit()
                    break

            if frame % SPEED == 0:
                self.solver.solve()

            self.screen.fill(BG_COLOR)
            self.board.render(self.screen)
            self.board.render_many(self.screen, self.solver.closedset)
            self.board.render_one(self.screen, self.current)
            self.mouse.render(self.screen)
            self.render_text(fontoffset)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Main().run()
