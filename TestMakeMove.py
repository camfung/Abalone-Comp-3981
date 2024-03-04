from gameplay import Game, GameState, Move
from enums import *


game = Game(Formation.DEFAULT)
print(game)
moves = game.get_current_game_state().get_possible_moves()

move = Move((7, 3), (7, 5), Direction.UP_RIGHT,
            Marble.BLACK, MarbleSelection.HORIZONTAL)
print(move)
game.set_move(Marble.BLACK, move)

move = Move((1, 5), (3, 5), Direction.DOWN_RIGHT,
            Marble.WHITE, MarbleSelection.BACKWARD_SLASH)

game.set_move(Marble.WHITE, move)

print(game)
move = Move((6, 4), (6, 6), Direction.UP_RIGHT,
            Marble.BLACK, MarbleSelection.HORIZONTAL)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((8, 2), (8, 4), Direction.UP_RIGHT,
            Marble.BLACK, MarbleSelection.HORIZONTAL)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((7, 3), (7, 5), Direction.UP_RIGHT,
            Marble.BLACK, MarbleSelection.HORIZONTAL)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((2, 5), (4, 5), Direction.DOWN_RIGHT,
            Marble.WHITE, MarbleSelection.BACKWARD_SLASH)
game.set_move(Marble.WHITE, move)
print(game)
