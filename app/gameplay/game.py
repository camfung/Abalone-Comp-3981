
from app.api.enums import *
from app.api.records import RecordHistory
from app.api.exceptions import InvalidMarbleValue
import csv
from app.gameplay.game_state import GameState


class Game:
    """
    Represents a game of Abalone, including its configuration, state, and history of moves.
    """

    id_counter = 0

    def __init__(self, formation: Formation):
        """
        Initializes a new game with a specific board formation.

        Parameters:
        - formation: The starting formation of the game as defined by the Formation enum.
        """
        Game.id_counter += 1
        self._game_id = Game.id_counter
        self._current_game_state = Game.initialize_board_layout(formation)
        self._record_history = RecordHistory(self._game_id)

    @staticmethod
    def initialize_board_layout(formation: Formation):
        """
        Initializes the board layout based on the specified formation.

        Parameters:
        - formation: The formation to use for initializing the board, specified as a value from the Formation enum.

        Returns:
        A GameState object representing the initialized game state.
        """
        starting_board = [[None, None, None, None,
                           None, None, None, None, None, None, None]]
        file = None
        csv_reader = None

        if formation == Formation.DEFAULT:
            file = open('./app/formations/default.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        elif formation == Formation.BELGIAN_DAISY:
            file = open('./app/formations/belgian_daisy.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        elif formation == Formation.GERMAN_DAISY:
            file = open('./app/formations/german_daisy.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        for row in csv_reader:
            formatted_row = []
            for item in row:
                if item in "None":
                    formatted_row.append(None)
                elif item in "WHITE":
                    formatted_row.append(Marble.WHITE)
                elif item in "BLACK":
                    formatted_row.append(Marble.BLACK)
                elif item in "EMPTY":
                    formatted_row.append(Marble.NONE)
                else:
                    raise InvalidMarbleValue(
                        f"{item} is not a valid marble value.")
            starting_board.append(formatted_row)

        file.close()

        starting_board.append(
            [None, None, None, None, None, None, None, None, None, None, None])
        return GameState(starting_board)

    def get_current_game_state(self) -> GameState:
        return self._current_game_state

    def get_possible_game_states(self):
        return self._current_game_state.convert_moves_to_game_states()

    def set_move(self, player=None, move=None, timestamp=None):
        """
        Updates the game state with a new move.

        Parameters:
        - player: The player making the move.
        - move: The Move object representing the move to be made.
        - timestamp: The timestamp when the move was made.
        """
        if player is None and move is None and timestamp is None:
            self._current_game_state = self._current_game_state.get_previous_game_state()
            self._record_history.remove_last_record()
            return

        next_marble = self._current_game_state.get_current_move_color()
        if next_marble is Marble.BLACK:
            next_marble = Marble.WHITE
        elif next_marble is Marble.WHITE:
            next_marble = Marble.BLACK
        else:
            raise InvalidMarbleValue("No Marble Value provided in Set Move.")
        print(f"{self._current_game_state.get_current_move_color()}: {move}")

        new_board_state = self._current_game_state.generate_new_board_state(
            move)
        new_game_state = GameState(new_board_state,
                                   next_marble,
                                   self._current_game_state)
        self._current_game_state = new_game_state
        self._record_history.add_record(move, player, timestamp)

    def get_ball_count(self):
        return self._current_game_state.get_ball_count()

    def get_record_history(self):
        return self._record_history

    def export_record_history(self):
        """
        Exports the record history of the game to a file.
        """
        self._record_history.export_records()

    def set_game_state(self, new_game_state):
        self._current_game_state = new_game_state

    def get_possible_moves(self):
        return self._current_game_state.get_possible_moves()

    def __str__(self):
        game_state_str = str(self._current_game_state)
        return f"Game ID: {self._game_id}\n{game_state_str}"
