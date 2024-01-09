from random import random, randint


class Solver:
    def __init__(self, game):
        self.cells = game.board.cells
        self.game = game
        self.closed = []

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
        return result

    def valid_cols(self, cell, result):
        x = cell.x
        y = cell.y

        for j in range(9):
            if y == j:
                continue
            other = self.cells[j][x]
            if other.value in result:
                result.remove(other.value)
        return result

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
        return result

    def backtrack(self, curr):
        if len(self.closed) <= 0:
            self.game.state = 3
            return
        curr.chosen = []
        prev = self.closed.pop()
        prev.value = 0

    def solve(self):
        if self.game.state in [0, 2, 3]:
            return
        curr = self.getEmpty()
        if not curr:
            self.game.state = 2
            return
        self.game.current = curr

        validValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for val in curr.chosen:
            if val in validValues:
                validValues.remove(val)
        self.valid_rows(curr, validValues)
        self.valid_cols(curr, validValues)
        self.valid_subgrid(curr, validValues)

        if len(validValues) == 0:
            return self.backtrack(curr)

        randIdx = randint(0, len(validValues) - 1)
        curr.value = validValues[randIdx]
        curr.chosen.append(curr.value)
        self.closed.append(curr)
