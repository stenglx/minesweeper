import z3
from ProbabilitySolver import Prob_Solver

class SAT_Solver():
    def __init__(self, board):
        self.board = board
        self.name = "SAT Solver"

    # inspired by https://sat-smt.codes/SAT_SMT_by_example.pdf page 50/51
    def getMove(self):
        #board_r = [[False for row in range(self.board.height)] for column in range(self.board.width)]
        board_r = [[False for column in range(self.board.width)] for row in range(self.board.height)]
        for i in range(self.board.height):
            for j in range(self.board.width):
                board_r[i][j] = self.board.board_public[i][j]

        board_r = SAT_Solver.reduceBombCountSAT(self,
                                              board_r)  # if bomb is placed -> reduce count of surrounding by 1 as risk is reduced
        for row in range(self.board.height):
            for column in range(self.board.width):
                if self.board.board_public[row][column] != '.':
                    continue
                solver = z3.Solver()
                # the following line is similar to https://sat-smt.codes/SAT_SMT_by_example.pdf page 50/51
                #placeholders = [[z3.Int('cell_%d_%d' % (r, c)) for r in range(self.board.height)] for c in range(self.board.width)]
                placeholders = [[z3.Int('cell_%d_%d' % (row, column)) for column in range(self.board.width)] for row in range(self.board.height)]
                # set mine to test
                solver.add(placeholders[row][column] == 1)
                for r in range(self.board.height):
                    for c in range(self.board.width):
                        solver.add(z3.Or(placeholders[r][c] == 1, placeholders[r][c] == 0))

                coords = self.getCoords( row, column, placeholders)
                rule = 0 # slowly increment rule
                # add values of all cell fields to rule
                for pair in coords:
                    row = pair[0]
                    column = pair[1]
                    # print(row,column)
                    rule += placeholders[row][column]

                board_value = self.board.board_public[row][column]
                if board_value == 'X':
                    continue
                solver.add(rule == board_value)
                if solver.check() == z3.unsat:
                    #print('Found safe cell')
                    # don't use field where no information is present
                    # sometimes those are considered
                    if self.safeArea(row, column, board_r) or self.AllMinesDiscovered():
                        return row, column
        return Prob_Solver.getMove(self)

    def getCoords(self, row, column, placeholders):
        counter_bombs = 0
        rule_attributes_coords = []
        for i in range(-1,2):
            for j in range(-1, 2):
                # go around field and get data
                r = row+i
                c = column + j
                if 0 <= r <= self.board.height - 1 and 0 <= c <= self.board.width - 1:
                    # skip identicals
                    if i == 0 and j == 0:
                        continue
                    neighbor_value = self.board.board_public[r][c]
                    if neighbor_value == 'X':
                        counter_bombs += 1

                    rule_attributes_coords.append([r, c])

        return rule_attributes_coords

    def safeArea(self, row,column, board_r):
        counter = 0
        counter_bombs = 0
        counter_neighbors = 0
        sum = 0
        for i in range(-1,2):
            for j in range(-1, 2):
                # go around field and get data
                r = row+i
                c = column + j
                # r und c im Bereich
                if 0 <= r <= self.board.height - 1 and 0 <= c <= self.board.width - 1:
                    # skip identicals
                    if i == 0 and j == 0:
                        continue
                    counter_neighbors += 1
                    neighbor_value = self.board.board_public[r][c]
                    neighbor_value_r = board_r[r][c]
                    if neighbor_value == '.':
                        counter +=1
                    if neighbor_value == 'X':
                        counter_bombs += 1
                    else:
                        # if adjacent cell is 0 there can't be a mine at cell
                        if neighbor_value == 0 or neighbor_value_r == 0:
                            return True
                        sum += neighbor_value
        return False

    def AllMinesDiscovered(self):
        counter_discovered_bombs = self.board.getCountOfDiscoveredMines()
        # all mines discovered = safe cell
        if counter_discovered_bombs == self.board.amount_mines:
            print('All mines discovered')
            return True

    def reduceBombCountSAT(self, board):
        for i in range(self.board.height):
            for j in range(self.board.width):
                cell = board[i][j]
                if cell == 'X':
                    coords = self.getCoordsSurrounding(i, j)
                    for pair in coords:
                        r = pair[0]
                        c = pair[1]
                        cell = board[r][c]
                        if cell != 'X' and cell != '.':
                            board[r][c] = board[r][c] - 1

        return board


    def getCoordsSurrounding(self, row, column):
        counter_bombs = 0
        rule_attributes_coords = []
        for i in range(-1,2):
            for j in range(-1, 2):
                # go around field and get data
                r = row+i
                c = column + j
                if 0 <= r <= self.board.height - 1 and 0 <= c <= self.board.width - 1:
                    # skip identicals TODO
                    if i == 0 and j == 0:
                        continue
                    #print('Surrounder', row+i, column+j)
                    neighbor_value = self.board.board_public[r][c]
                    #print(neighbor_value)
                    if neighbor_value == 'X':
                        counter_bombs += 1
                    rule_attributes_coords.append([r, c])

        return rule_attributes_coords


