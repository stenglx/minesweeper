import z3
from RandomAI import RandomSolver

import numpy as np

class Prob_Solver():
    def __init__(self, board):
        self.board = board
        self.name = 'Probability Solver'

    def getMove(self):
        coords_and_probabilities = []
        counter_unknown = 0
        counter_bomb = 0
        sum = 0
        #board_r = [[False for row in range(self.board.height)] for column in range(self.board.width)]
        board_r = [[False for column in range(self.board.width)] for row in range(self.board.height)]
        for i in range(self.board.height):
            for j in range(self.board.width):
                board_r[i][j] = self.board.board_public[i][j]

        board_r = Prob_Solver.reduceBombCount(self, board_r)  # if bomb is placed -> reduce count of surrounding by 1 as risk is reduced

        safe_cells =[]

        for row in range(self.board.height):
            for column in range(self.board.width):
                if self.board.board_public[row][column] != '.':
                    continue
                coords = Prob_Solver.getCoordsP(self,row,column)
               # print('rc', row, column, coords)
                for pair in coords:
                    r = pair[0]
                    c = pair[1]
                    val = board_r[r][c] # available X numbers
                    if val == '.':
                        counter_unknown += 1
                    elif val == 'X':
                        counter_bomb += 1
                    else:
                        if val == 0:
                            # choose field where adjacent nr says 0 mines -> no mine can be here
                            safe_cells.append([row,column])
                        sum += val

                prob = sum*100 + counter_unknown * 50
                prob = prob / len(coords)
                coords_and_probabilities.append([prob, row,column])
        np.sort(coords_and_probabilities, axis=0)

        if len(safe_cells) > 0:
            return safe_cells[0][0], safe_cells[0][1]
        for move in coords_and_probabilities:
            r = move[1]
            c= move[2]
            return r,c
        return RandomSolver.getMove(self)


    def getCoordsP(self, row, column):
        counter_bombs = 0
        rule_attributes_coords = []
        #print(row,column)
        for i in range(-1,2):
            for j in range(-1, 2):
                # go around field and get data
                r = row+i
                c = column + j
                if 0 <= r <= self.board.height - 1 and 0 <= c <= self.board.width - 1:
                    # skip identicals TODO
                    if i == 0 and j == 0:
                        continue
                    neighbor_value = self.board.board_public[r][c]
                    if neighbor_value == 'X':
                        counter_bombs += 1
                    rule_attributes_coords.append([r, c])

        return rule_attributes_coords


    def reduceBombCount(self, board):
        for i in range(self.board.height):
            for j in range(self.board.width):
                cell = board[i][j]
                if cell == 'X':
                    coords = Prob_Solver.getCoordsP(self, i, j)
                    for pair in coords:
                        r = pair[0]
                        c = pair[1]
                        cell = board[r][c]
                        if cell != 'X' and cell != '.':
                            board[r][c] = board[r][c] - 1

        return board

    def reduceBombCountField(self, board, i, j):
        coords = Prob_Solver.getCoordsP(self, i, j)
        for pair in coords:
            r = pair[0]
            c = pair[1]
            cell = board[r][c]
            if cell != 'X' and cell != '.':
                board[r][c] = board[r][c] - 1

        return board

    def improveBombCountField(self, board, i, j):
        coords = Prob_Solver.getCoordsP(self, i, j)
        for pair in coords:
            r = pair[0]
            c = pair[1]
            cell = board[r][c]
            if cell != 'X' and cell != '.':
                board[r][c] = board[r][c] + 1

        return board