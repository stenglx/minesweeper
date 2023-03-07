from ProbabilitySolver import Prob_Solver

# inspired by https://www.geeksforgeeks.org/minesweeper-solver/
class Backtrack_Solver():
    def __init__(self, board):
        self.board = board
        self.name = "Backtracking Solver"
        self.mines_available = self.board.amount_mines

    def getMove(self):
        #visited_fields = [[False for row in range(self.board.height)] for column in range(self.board.width)]
        #mine_grid = [[False for row in range(self.board.height)] for column in range(self.board.width)]
        #board_reduced = [[False for row in range(self.board.height)] for column in range(self.board.width)]
        visited_fields = [[False for column in range(self.board.width)] for row in range(self.board.height)]
        mine_grid = [[False for column in range(self.board.width)] for row in range(self.board.height)]
        board_reduced = [[False for column in range(self.board.width)] for row in range(self.board.height)]
        for i in range(self.board.height):
            for j in range(self.board.width):
                board_reduced[i][j] = self.board.board_public[i][j]
                if self.board.board_public[i][j] == 'X':
                    self.mines_available = self.mines_available - 1

        board_reduced = self.reduceBombCount(board_reduced) # if bomb is placed -> reduce count of surrounding by 1 as risk is reduced

        # set already known mines to true
        for row in range(self.board.height):
            for column in range(self.board.width):
                if self.board.board_public[row][column] == 'X':
                    mine_grid[row][column] = True

        retval, mine_grid, visited_fields = self.return_Solution(self.board.board_public, visited_fields, mine_grid,
                                                                 self.board.amount_mines, board_reduced)

        if retval:
            # look for safe cell to return
            for row in range(self.board.height):
                for column in range(self.board.width):
                    # found a bomb which is hidden
                    # cell can be chosen and backtracking resulted in it being no mine
                    # return this cell
                    if self.board.board_public[row][column] == '.' and mine_grid[row][column] == False:
                        print('Return move from backtracking')
                        return row, column
        return Prob_Solver.getMove(self)

    def return_Solution(self, board, visited_fields, mine_grid, iterations, board_r):
        if self.AllBombsFound(mine_grid):
            return True, mine_grid, visited_fields
        # if all cells are visited but not all bombs found -> no solution
        if self.AllVisited(visited_fields) and not self.AllBombsFound(mine_grid):
            return False, mine_grid, visited_fields

        # try placing mines until solution for all placements is found
        for row in range(self.board.height):
            for column in range(self.board.width):
                # mine can't be place when already taken
                if visited_fields[row][column]:
                    continue # to not go into none result bringing fields again
                if board[row][column] != '.':
                    visited_fields[row][column] = True
                    continue
                visited_fields[row][column] = True
                if self.cellCanBeBomb(row, column, board_r):
                    # set mine to current row/col
                    mine_grid[row][column] = True
                    board_r[row][column] = 'X'
                    # after mine is set reduce board_r value of adjacent neighbors
                    board_r = self.reduceBombCountField(board_r, row, column)  # if bomb is placed -> reduce count of surrounding by 1 as risk is reduced

                    # Recursive Call
                    if self.return_Solution(board, visited_fields, mine_grid, iterations, board_r):
                        return True, mine_grid, visited_fields

                    # if recursive call with set mine failed -> reset to state before call to backtrack and try another step
                    mine_grid[row][column] = False
                    board_r[row][column] = '.'
                    board_r = self.improveBombCountField(board_r, row, column)
                # recursive call without mine being set
                if self.return_Solution(board, visited_fields, mine_grid, iterations, board_r):
                    return True, mine_grid, visited_fields
                # visited field doesn't lead to any result and therefore we delete the try
                visited_fields[row][column] = False
        return False, mine_grid, visited_fields

    def cellCanBeBomb(self, row, column, board_r):
        coords = self.getCoordsB(row, column)
        for pair in coords:
            r = pair[0]
            c = pair[1]
            cell = board_r[r][c]
            if cell == 'X':
                continue
            elif cell == '.':
                continue
            else:
                # if surrounding has value 0 the cell can't be a bomb!
                if cell == 0:
                    return False
        return True

    # done if all bombs found and all fields visited
    def AllBombsFound(self, board):
        bomb_counter = 0
        for row in range(self.board.height):
            for column in range(self.board.width):
                if board[row][column] == 'X':
                    bomb_counter += 1
        if bomb_counter == self.board.amount_mines:
            return True
        return False

        # done if all bombs found and all fields visited

    def AllVisited(self, visited):
        for row in range(self.board.height):
            for column in range(self.board.width):
                if not visited[row][column]:
                    return False
        return False

    def getCoordsB(self, row, column):
        counter_bombs = 0
        rule_attributes_coords = []
        # print(row,column)
        for i in range(-1, 2):
            for j in range(-1, 2):
                # go around field and get data
                r = row + i
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

    def reduceBombCount(self, board):
        for i in range(self.board.height):
            for j in range(self.board.width):
                cell = board[i][j]
                if cell == 'X':
                    coords = self.getCoordsB(i, j)
                    for pair in coords:
                        r = pair[0]
                        c = pair[1]
                        cell = board[r][c]
                        if cell != 'X' and cell != '.':
                            board[r][c] = board[r][c] - 1

        return board

    def reduceBombCountField(self, board, i, j):
        coords = self.getCoordsB(i, j)
        for pair in coords:
            r = pair[0]
            c = pair[1]
            cell = board[r][c]
            if cell != 'X' and cell != '.':
                board[r][c] = board[r][c] - 1

        return board

    def improveBombCountField(self, board, i, j):
        coords = self.getCoordsB(i, j)
        for pair in coords:
            r = pair[0]
            c = pair[1]
            cell = board[r][c]
            if cell != 'X' and cell != '.':
                board[r][c] = board[r][c] + 1

        return board