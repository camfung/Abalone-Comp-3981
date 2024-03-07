
import abc
from gameplay import *
from exceptions import DuplicateSingletons


class GameManager():
    __instance = None

    @staticmethod
    def get_instance():
        if GameManager.__instance is None:
            GameManager.__instance = GameManager()
        return GameManager.__instance

    def __init__(self, app):
        if GameManager.__instance is not None:
            raise DuplicateSingletons(
                "Only one instance of GameManager can be created")

        self._app = app
        self._move_history = []
        self._observers = []
        self._game = None
        GameManager.__instance = self

    def commit_move(self, player, move, timestamp):
        self._move_history.append(copy.deepcopy(self._game.get_current_game_state()))
        self._game.set_move(player, move, timestamp)
        self.notify()

    def undo_last_move(self):
        if len(self._move_history) != 0:
            self._game.set_game_state(self._move_history.pop())
            self._game.get_record_history().remove_last_record()
            self.notify()
        else:
            pass

    @property
    def game_score(self):
        """
        Retrieves the current score of the game.

        This property provides access to the current score by returning a tuple
        containing the count of white balls and black balls in the game. It utilizes
        the current game state to fetch these values.

        Returns:
            tuple: A tuple where the first element is the count of white balls and
                the second element is the count of black balls in the game.
        """
        return (self._game._white_balls, self._game._black_balls)

    @property
    def current_player_to_move(self):
        return self._game.get_current_game_state().get_current_move_color()

    def get_possible_moves(self):
        return self._game.get_current_game_state().get_possible_moves()

    def get_board(self):
        return self._game.get_current_game_state().get_board()

    def start_game(self, formation):
        self._game = Game(formation)

    def stop_game(self):
        self._game.export_record_history()

    def pause_game(self):
        self.notify()

    def join_room(self, player):
        self._observers.append(player)

    def leave_room(self, player):
        self._observers.remove(player)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def get_record_history(self):
        return self._game.get_record_history()
