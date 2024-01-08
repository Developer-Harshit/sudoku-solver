# Basic Screen

import pygame
import sys

print("Starting Game")

from scripts.consts import BLUE, RED, BG_COLOR, FPS
from scripts.blob import Blob
from scripts.util import draw_circle


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku")

        self.screen = pygame.display.set_mode((960, 640), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        
        self.blob = Blob((0, 0), 10, RED, True)
        

    def run(self):
        running = True
        while running:
         
            
             # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                # Quit ------------------------------------------------------------|
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
            

            # For Background ------------------------------------------------------|
            self.screen.fill(BG_COLOR)

            # Mouse ---------------------------------------------------------------|
            self.blob.pos = list(pygame.mouse.get_pos())
            self.blob.render(self.screen)

            

           
            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(
                pygame.transform.scale(self.screen, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
print("Game Over")