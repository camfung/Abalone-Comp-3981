
from datetime import datetime, time


class Record:
    def __init__(self, index, game_id, move):
        self._index = index
        self._game_id = game_id
        self._move = move

    def get_game_id(self):
        return self._game_id

    def get_index(self):
        return self._index

    def get_move(self):
        return self._move


class RecordHistory:
    game_counter = 0

    def __init__(self, game_id):
        RecordHistory.game_counter += 1

        self._game_id = game_id
        self._records = []

    def get_game_id(self):
        return self._game_id

    def get_records(self):
        return self._records

    def get_record(self, index):
        return self._records[index]

    def add_record(self, move):
        self._records.append(Record(len(self._records) + 1, self._game_id, move))

    def remove_last_record(self):
        self._records.pop()

    def export_records(self):
        game_time = datetime.now()
        name = f"./games/{game_time} - {self._game_id}.txt"
        with open(name, 'w') as f:
            f.write(str(game_time))
            for record in self._records:
                move = record.get_move()

                try:
                    f.write(move)
                except Exception as e:
                    raise e
