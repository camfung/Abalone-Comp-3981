import json
from app.gameplay.game import Game
from app.gameplay.move import Move
from app.enums import *

# Function to convert direction text to Direction enum


def parse_direction(direction_str):
    direction_map = {
        "downright": Direction.DOWN_RIGHT,
        "down right": Direction.DOWN_RIGHT,
        "down left": Direction.DOWN_LEFT,
        # Add other directions as needed
    }
    return direction_map[direction_str.lower()]


# Initialize the game with a default formation
game = Game(Formation.DEFAULT)
print(game)

# Function to execute moves from a JSON file


def execute_moves_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        for move_data in data['moves']:
            start = tuple(move_data['start'])
            end = tuple(move_data['end'])
            direction = parse_direction(move_data['direction'])

            # Determine marble color based on some logic or use alternation
            marble_color = Marble.BLACK  # Example, you might want to alternate this

            # Create and execute the move
            move = Move(start, end, direction, marble_color)
            game.set_move(marble_color, move)

            # Print the board state
            print(game)


# Call the function with the path to your JSON file
execute_moves_from_json('moves.json')
input("press enter to exit")
