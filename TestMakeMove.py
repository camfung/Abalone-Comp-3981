from gameplay import Game, GameState, Move
from enums import Direction, Formation, Marble


game = Game(Formation.DEFAULT)
print(game)
moves = game.get_current_game_state().get_possible_moves()
input("press enter when your ready for a move to be made.")
move = Move((6, 3), (6, 5), Direction.UP_RIGHT, Marble.BLACK)
print(move)
game.set_move(Marble.BLACK, move)

print(game)
while True:
    pass
