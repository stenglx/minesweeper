## This class shall manage the board

import random
import itertools

class Minesweeper():
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        #self.grid_size = grid_size
        self.amount_mines = mines

        # fields the player sees
        #self.board_public = [['.' for row in range(height)] for column in range(width)]
        self.board_public = [['.' for column in range(width)] for row in range(height)]
        # private field to know values and bomb placements
        #self.board_private = [[0 for row in range(height)] for column in range(width)]
        self.board_private = [[0 for column in range(width)] for row in range(height)]

        # add mines and neighbor numbers to private board
        self.setMines()

        # remove later, only for selfcheck
        self.printBoard(self.board_private)

    def setMines(self):
        for i in range(self.amount_mines):
            row = random.randint(0, self.height-1)
            column = random.randint(0, self.width-1)
            if self.board_private[row][column] == 0:
                self.board_private[row][column] = 'X'
                self.addNumbersToSurrounding(row, column)

    def addNumbersToSurrounding(self, row, column):
        # Method to calculate the values of the tiles around the bombs
        # +1 for each bomb in the surrounding are of the cell
        # This method is inspired by the implementation of
        # https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de
        if 0 <= row <= self.height - 1:
            if 0 <= column <= self.width - 2:
                if self.board_private[row][column + 1] != 'X':
                    self.board_private[row][column + 1] += 1
            if 1 <= column <= self.width - 1:
                if self.board_private[row][column - 1] != 'X':
                    self.board_private[row][column - 1] += 1
        if 1 <= row <= self.height - 1:
            if 1 <= column <= self.width - 1:
                if self.board_private[row - 1][column - 1] != 'X':
                    self.board_private[row - 1][column - 1] += 1
            if 0 <= column <= self.width - 2:
                if self.board_private[row - 1][column + 1] != 'X':
                    self.board_private[row - 1][column + 1] += 1
            if 0 <= column <= self.width - 1:
                if self.board_private[row - 1][column] != 'X':
                    self.board_private[row - 1][column] += 1
        if row <= self.height - 2:
            if 0 <= column <= self.width - 2:
                if self.board_private[row + 1][column + 1] != 'X':
                    self.board_private[row + 1][column + 1] += 1
            if 1 <= column <= self.width - 1:
                if self.board_private[row + 1][column - 1] != 'X':
                    self.board_private[row + 1][column - 1] += 1
            if 0 <= column <= self.width - 1:
                if self.board_private[row + 1][column] != 'X':
                    self.board_private[row + 1][column] += 1

    # This method is not done by me, it's from following source:
    # https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de
    def printBoard(self, board):
        for row in board:
            print("\t".join(str(cell) for cell in row))
            print("")

    def checkIfGameWon(self):
        for row in self.board_public:
            for cell in row:
                #print(cell)
                if cell == '.':
                    return False
        return True

    def getCountOfDiscoveredMines(self):
        counter = 0
        for row in self.board_public:
            for cell in row:
                #print(cell)
                if cell == 'X':
                    counter += 1
        return counter

    def checkIfGameLost(self, row, column):
        if self.board_private[row][column] == 'X':
            return True
        return False

    def makeMove(self, row, column):
        if self.board_public[row][column] == '.':
            # show real field value
            self.board_public[row][column] = self.board_private[row][column]
            # show surrounding field values (reveal them)
            self.revealNeighbors(row, column)

    def revealNeighbors(self, row, column):
        # Method to reveal the values of the neighboring tiles around the chosen field
        # This method is inspired by the implementation of
        # https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de
        if 0 <= row <= self.height - 1:
            if 0 <= column <= self.width - 2:
                self.board_public[row][column + 1] =  self.board_private[row][column + 1]
            if 1 <= column <= self.width - 1:
                self.board_public[row][column - 1] =  self.board_private[row][column - 1]
        if 1 <= row <= self.height - 1:
            if 1 <= column <= self.width - 1:
                self.board_public[row - 1][column - 1] =  self.board_private[row - 1][column - 1]
            if 0 <= column <= self.width - 2:
                self.board_public[row - 1][column + 1] =  self.board_private[row - 1][column + 1]
            if 0 <= column <= self.width - 1:
                self.board_public[row - 1][column] =  self.board_private[row - 1][column]
        if row <= self.height - 2:
            if 0 <= column <= self.width - 2:
                self.board_public[row + 1][column + 1] =  self.board_private[row + 1][column + 1]
            if 1 <= column <= self.width - 1:
                self.board_public[row + 1][column - 1] =  self.board_private[row + 1][column - 1]
            if 0 <= column <= self.width - 1:
                self.board_public[row + 1][column] = self.board_private[row + 1][column]



