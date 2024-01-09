# Basic Screen

import pygame

print("Initializing")


from scripts.constants import SPEED, ORANGE, WHITE
from scripts.util import generate_text, msg, Mouse
from scripts.solver import Solver
from scripts.board import Board


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")

        dim = 720
        self.dim = dim
        self.screen = pygame.display.set_mode((dim, dim), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        self.mouse = Mouse()
        self.restart()
        self.current = self.board.cells[0][0]

    def restart(self):
        self.board = Board(self.dim)
        self.solver = Solver(self)
        self.state = 0

    def run(self):
        running = True
        frame = 0
        fontoff = self.board.size / 2
        while running:
            frame += 1
            # Calculate Current ----------------------------------------------------|
            mpos = pygame.mouse.get_pos()
            if self.state == 0:
                bpos = self.board.returnColliding(mpos)
                self.current = self.board.cells[bpos.y][bpos.x]

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Exiting")
                        running = False
                    if event.key == pygame.K_r:
                        print("Restarting")
                        self.restart()

                    if event.key == pygame.K_s and self.state == 0:
                        print("Starting")
                        self.state = 1
                    # Fill Digit ---------------------------------------------------|
                    if self.state == 0:
                        digit = event.key - 48
                        if digit > -1 and digit < 10:
                            self.current.value = digit

                # Quit ------------------------------------------------------------|
                if event.type == pygame.QUIT:
                    print("Exiting")
                    running = False

            # For Background ------------------------------------------------------|
            self.screen.fill(WHITE)

            if frame % SPEED == 0:
                self.solver.solve()
            # Board ---------------------------------------------------------------|
            self.board.render(self.screen)
            self.board.render_many(self.screen, self.solver.closed)
            self.board.render_one(self.screen, self.current)

            # Mouse ---------------------------------------------------------------|
            self.mouse.pos = list(mpos)
            self.mouse.render(self.screen)

            # Message -------------------------------------------------------------|
            # bottom text
            mytext = msg[self.state]
            tSize = mytext.get_size()

            self.screen.blit(
                mytext,
                (
                    (self.dim / 2 - tSize[0] / 2, self.dim + tSize[1] / 2 - fontoff),
                    tSize,
                ),
            )

            # top text
            if self.state == 0:
                mytext = msg[4]
                tSize = mytext.get_size()

                self.screen.blit(
                    mytext,
                    ((self.dim / 2 - tSize[0] / 2, fontoff + tSize[1] / 2), tSize),
                )
                pass
            else:
                mytext = msg[5]
                tSize = mytext.get_size()
                self.screen.blit(
                    mytext,
                    ((self.dim / 2 - tSize[0] / 2, fontoff + tSize[1] / 2), tSize),
                )
                pass

            # Rendering Screen ----------------------------------------------------|
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
