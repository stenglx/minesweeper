# main class to run game
from boardClass import Minesweeper
from RandomAI import RandomSolver
from ProbabilitySolver import Prob_Solver
from SATSolver import SAT_Solver
from BacktrackSolver import Backtrack_Solver

def runGame(game, solver):
    # make init move to reveal a few fields to get better chances for AI
    game.printBoard(game.board_public)
    game.makeMove(1, 1)
    game.makeMove(game.height - 2, game.width - 2)

    game.printBoard(game.board_public)

    # main game loop
    while True:

        won = game.checkIfGameWon()
        if won:
            print('YEY GAME WON YEY')
            return 1

        # get move from solver
        row, column = solver.getMove()
        print('Returnd Move', row, column)
        game.makeMove(row, column)

        lost = game.checkIfGameLost(row, column)
        if lost:
            game.printBoard(game.board_public)
            print(':( GAME LOST :(')
            return 0

        game.printBoard(game.board_public)


if __name__== '__main__':
    accuracy = 0

    mines = 8
    #mines = 40
    #height = 8
    #width = 8
    #height = 16
    #width = 16
    height = 10
    width = 4

    #nr_of_games = 50
    nr_of_games = 5

    for i in range(nr_of_games):
        game = Minesweeper(height, width, mines)
        # TODO choose the solver you want
        solver = RandomSolver(game)
        solver = Prob_Solver(game)
        solver = SAT_Solver(game)
        solver = Backtrack_Solver(game)


        accuracy += runGame(game, solver)

    print('For this statistic calculation ', nr_of_games, 'were played')
    print('The agent has a win ratio of', accuracy*100/nr_of_games, 'on a field of size', height, 'x', width, 'with ', mines, 'hidden mines')
    print('The solver used was called', solver.name)



