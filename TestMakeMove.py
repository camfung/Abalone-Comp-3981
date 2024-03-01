from gameplay import Game, GameState, Move
from enums import Direction, Formation, Marble


game = Game(Formation.DEFAULT)
print(game)

input("press enter when your ready for a move to be made.")
move = Move((1, 5), (3, 5), Direction.UP_LEFT, Marble.BLACK)

game.set_move(Marble.BLACK, Move)

print(game)
while True:
    pass
