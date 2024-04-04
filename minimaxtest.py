import time
from app.api.enums import Formation, Marble
from app.communication.game_manager import GameManager
from app.gameplay.game import Game
from app.players.agent import AbaloneAgent
from app.players.test_agents.cameron import AgentCameron
from test import getBoardStateFromFile
from app.gameplay.game_state import GameState


# gameState = getBoardStateFromFile("TestBoard.txt")
game = Game(Formation.DEFAULT)
gameState = game.get_current_game_state()

# print(gameState)

gameManager = GameManager(None, gameState)

player = AgentCameron(100, 100, Marble.BLACK)

move = player.calc_move(gameManager, None)
print(move, "test")

gameManager.commit_move(Marble.BLACK, move, time.time())
print(gameManager.get_current_game_state())
input("Press Enter to continue...")
