import copy
import csv
import datetime
import math
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


def timeStateSpace(gameManager):
    player = AbaloneAgent(100, 100, Marble.BLACK)
    start = datetime.datetime.now()
    move = player.generate_move(gameManager, start)
    end = datetime.datetime.now()
    print(move)
    end_time = end-start
    print(end_time)
    return end_time


game = Game(Formation.DEFAULT)
gameState = game.get_current_game_state()
# gameState = getBoardStateFromFile("TestBoard.txt")
gameManager = GameManager(None, gameState)
timeStateSpace(gameManager)

times = []
for i in range(10):
    times.append((i, timeStateSpace(gameManager)))
for time in times:
    print(time[0], time[1])
input()
