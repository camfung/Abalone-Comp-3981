
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
        self._observers = []
        self._game = None
        GameManager.__instance = self

    def commit_move(self, player, move):
        self._game.set_move(player, move)
        self.notify()

    def undo_last_move(self):
        self._game.set_move()
        self.notify()

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

    def commit_move(self, player, move, timestamp):
        self._game.set_move(player, move, timestamp)
        self.notify()

    def leave_room(self, player):
        self._observers.remove(player)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def get_record_history(self):
        return self._game.get_record_history()
