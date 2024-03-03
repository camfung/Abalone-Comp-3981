from gameplay import Game, GameState, Move
from enums import Direction, Formation, Marble


game = Game(Formation.DEFAULT)
print(game)
moves = game.get_current_game_state().get_possible_moves()
move = Move((7, 3), (7, 5), Direction.UP_RIGHT, Marble.BLACK)
print(move)
game.set_move(Marble.BLACK, move)

move = Move((1,5), (3,5), Direction.DOWN_RIGHT, Marble.WHITE)

game.set_move(Marble.WHITE, move)
print(game)
