
from datetime import datetime, time


class Record:
    def __init__(self, index, game_id, move, turn, timestamp):
        self._index = index
        self._game_id = game_id
        self._move = move
        self._player_turn = turn
        self._time_taken = timestamp

    def get_game_id(self):
        """
        Get the game id the record belongs to
        :return: integer
        """
        return self._game_id

    def get_index(self):
        """
        Gets the index of the record within the records
        :return: integer
        """
        return self._index

    def get_move(self):
        """
        Gets the move recorded.
        :return: Move
        """
        return self._move

    def __str__(self):
        """
        A pretty string representation of the Record.
        :return: String including index, player turn, move and timestamp
        """
        return f"{self._index}: {self._player_turn} {self._move} - {int(self._time_taken)} seconds"


class RecordHistory:
    game_counter = 0

    def __init__(self, game_id):
        RecordHistory.game_counter += 1

        self._game_id = game_id
        self._records = []

    def get_game_id(self):
        """
        Returns the Game ID of this RecordHistory
        :return: integer
        """
        return self._game_id

    def get_records(self):
        """
        Gets the full list of records
        :return: Record[]
        """
        return self._records

    def get_record(self, index):
        """
        Gets a Record of Index from List of Records
        :param index: integer
        :return: Record
        """
        return self._records[index]

    def add_record(self, move, turn, timestamp):
        """
        Adds a new record to the list of existing records
        :param move: Move
        :param turn: Marble Color
        :param timestamp: Time Calculated
        :return:
        """
        self._records.append(Record(len(self._records) + 1, self._game_id, move, turn, timestamp))

    def remove_last_record(self):
        """
        Removes the last record from the list of existing records.
        Most likely used in undo move.
        :return:
        """
        self._records.pop()

    def export_records(self):
        """
        Exports the list of records to a text file.
        :return:
        """
        game_time = datetime.now()
        name = f"./games/{game_time} - {self._game_id}.txt"
        with open(name, 'w') as f:
            f.write(str(game_time))
            for record in self._records:
                try:
                    f.write(record)
                except Exception as e:
                    raise e
