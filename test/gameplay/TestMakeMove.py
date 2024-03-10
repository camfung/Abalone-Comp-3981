
from app.gameplay.game import Game
from app.gameplay.move import Move
from app.enums import *


game = Game(Formation.DEFAULT)
print(game)
moves = game.get_current_game_state().get_possible_moves()

move = Move((7, 3), (7, 5), Direction.UP_RIGHT,
            Marble.BLACK)
print(move)
game.set_move(Marble.BLACK, move)

move = Move((1, 5), (3, 5), Direction.DOWN_RIGHT,
            Marble.WHITE)

game.set_move(Marble.WHITE, move)

print(game)
move = Move((6, 4), (6, 6), Direction.UP_RIGHT,
            Marble.BLACK)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((8, 2), (8, 4), Direction.UP_RIGHT,
            Marble.BLACK)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((7, 3), (7, 5), Direction.UP_RIGHT,
            Marble.BLACK)
game.set_move(Marble.BLACK, move)

print(game)

move = Move((2, 5), (4, 5), Direction.DOWN_RIGHT,
            Marble.WHITE)
game.set_move(Marble.WHITE, move)
print(game)
