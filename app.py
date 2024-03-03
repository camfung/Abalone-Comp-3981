from enums import Formation
from gameplay import Game
from communication import GameManager
from ui import HUD, Board, PygameUI


class App:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.game = GameManager()
            cls.game.start_game(Formation.DEFAULT)
            cls.gui = PygameUI()
            hud = HUD()
            board = Board()

            # add the drawables
            cls.gui.drawable_elements.append(hud)
            cls.gui.drawable_elements.append(board)

            # add the event handlers
            cls.gui.event_handlers.append(hud)
            cls.gui.event_handlers.append(board)
        return cls._instance

    def run(self):
        self.gui.run(self.game)
