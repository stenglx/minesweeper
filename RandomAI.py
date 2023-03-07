import random

class RandomSolver:
    name = "Random Solver"

    def __init__(self, board):
        self.board = board
        self.name = "Random Solver"

    def getMove(self):
        # try out randoms until one cell with no value set yet is found
        while True:
            row = random.randint(0, self.board.height -1)
            column = random.randint(0, self.board.width - 1)
            if self.board.board_public[row][column] == '.':
                return row,column
