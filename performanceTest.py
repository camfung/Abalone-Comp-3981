import copy
import csv
import datetime
import time
from app.api.enums import Formation, Marble
from app.api.exceptions import InvalidMarbleValue
from app.communication.game_manager import GameManager
from app.gameplay.game import Game
from app.gameplay.timer import Timer
from app.players.agent import AbaloneAgent
from app.players.test_agents.cameron import AgentCameron
from app.gameplay.game_state import GameState
import cProfile
import pstats


def getBoardStateFromFile(input_file):
    # Step 1: Read Input File
    with open(input_file, "r") as input_f:
        # Step 2: Read Current Player's Turn
        r_current_player = input_f.readline().strip()
        if r_current_player == "b":
            current_player = Marble.BLACK
        elif r_current_player == "w":
            current_player = Marble.WHITE

        # Step 3: Read Board Configuration
        r_board_config = input_f.readline().strip()
        board_spots = r_board_config.split(",")

        file = open('app/formations/blank_board.csv', 'r')
        csv_reader = csv.reader(file, delimiter=',')

        starting_board = [[None, None, None, None,
                           None, None, None, None, None, None, None]]

        for row in csv_reader:
            formatted_row = []
            for item in row:
                if item in "None":
                    formatted_row.append(None)
                elif item in "EMPTY":
                    formatted_row.append(Marble.NONE)
                else:
                    raise InvalidMarbleValue(
                        f"{item} is not a valid marble value.")
            starting_board.append(formatted_row)

        starting_board.append(
            [None, None, None, None, None, None, None, None, None, None, None])

        file.close()

        for board_spot in board_spots:
            int_val = ord(board_spot[0])
            row = (int_val - 74) * -1
            col = int(board_spot[1])
            r_marble = board_spot[2]
            if r_marble == "b":
                marble = Marble.BLACK
            elif r_marble == "w":
                marble = Marble.WHITE
            starting_board[row][col] = marble

    # Step 4: Create New GameState from the Board Configuration (Step 3) & Current Player's Turn (Step 2)
    start_state = GameState(starting_board, current_player)
    return start_state


def simulate_game():
    gameState = getBoardStateFromFile("TestBoard.txt")
    # game = Game(Formation.DEFAULT)
    # gameState = game.get_current_game_state()

    gameManager = GameManager(None, gameState)

    player1 = AgentCameron(20, 100, Marble.BLACK)
    player2 = AgentCameron(20, 100, Marble.WHITE)

    gameOver = False
    times = []
    i = 0
    print(gameManager.get_current_game_state())
    while not gameOver:
        startTime = datetime.datetime.now()
        move = player1.calc_move(gameManager, datetime.datetime.now())
        print("player1 move: ", move)
        gameManager.commit_move(Marble.BLACK, move, time.time())
        move = player2.calc_move(gameManager, datetime.datetime.now())
        print("player2 move: ", move)
        gameManager.commit_move(Marble.WHITE, move, time.time())
        endTime = datetime.datetime.now()
        totalTime = endTime - startTime
        print(totalTime)
        times.append((i, totalTime.total_seconds()))
        print(gameManager.get_current_game_state())
        i += 1
        if i > 40:  # or any other condition to end the game
            gameOver = True

    # Optionally, print the times for each move
    for b in times:
        print(b)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    simulate_game()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()

# gameState = getBoardStateFromFile("testboard.txt")

# game = Game(Formation.DEFAULT)
# gameState = game.get_current_game_state()

# # print(gameState)
# start = datetime.datetime.now()
# gameManager = GameManager(None, gameState)
# gameManager.get_current_game_state().generate_possible_moves()
# end = datetime.datetime.now() - start
# print(end)
# player1 = AgentCameron(100, 100, Marble.BLACK)
# player2 = AgentCameron(100, 100, Marble.WHITE)

# print(gameState)
# board_dict = player1.get_board_dict(gameState.get_board())
# cohesion = player1.calculate_cohesion(board_dict)
# print(cohesion)
# input()
# timer = Timer()
# timer._white_turn_time_limit = 5
# timer._black_turn_time_limit = 5

# gameOver = False
# times = []
# i = 0
# while not gameOver:
#     startTime = datetime.datetime.now()
#     move = player1.calc_move(gameManager, timer)
#     gameManager.commit_move(Marble.BLACK, move, time.time())
#     move = player2.calc_move(gameManager, timer)
#     gameManager.commit_move(Marble.WHITE, move, time.time())
#     endTime = datetime.datetime.now()
#     totalTime = endTime - startTime
#     times.append((i, totalTime.total_seconds()))
#     print(totalTime.total_seconds())
#     i += 1
#     print(gameManager.get_current_game_state())
#     if i > 90:
#         gameOver = True
# for b in times:
#     print(b, ",", sep="")
# input("Press Enter to continue...")

a = (1, 2)
b = (3, 4)
a = copy.deepcopy(b)
