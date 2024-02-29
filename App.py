from players import GameManager
from ui import HUD, Board, PygameUI


class App:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.game = GameManager()
            cls.gui = PygameUI()

            cls.gui.elements.append(HUD())
            cls.gui.elements.append(Board())
        return cls._instance

    def run(self):
        self.gui.run()
