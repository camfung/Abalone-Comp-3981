
import abc
from gameplay import *
from exceptions import DuplicateSingletons


class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Observable(abc.ABC):
    @abc.abstractmethod
    def join_room(self, player):
        pass

    @abc.abstractmethod
    def leave_room(self, player):
        pass

    @abc.abstractmethod
    def notify(self):
        pass


class GameManager(Observable):
    __instance = None

    @staticmethod
    def get_instance():
        if GameManager.__instance is None:
            GameManager.__instance = GameManager()
        return GameManager.__instance

    def __init__(self):
        if GameManager.__instance is not None:
            raise DuplicateSingletons("Only one instance of GameManager can be created")

        self._observers = []
        self._game = None
        GameManager.__instance = self

    def join_room(self, player):
        self._observers.append(player)

    def leave_room(self, player):
        self._observers.remove(player)

    def notify(self):
        for observer in self._observers:
            observer.update()

    def start_game(self, formation):
        self._game = Game(formation)

    def stop_game(self):
        self._game.export_record_history()

    def pause_game(self):
        pass

    def undo_last_move(self):
        self._game.set_move()
        self.notify()
