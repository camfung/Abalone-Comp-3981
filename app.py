from enums import Formation, GameType, Marble
from gameplay import Game, Move
from communication import GameManager
from players import AbaloneAgent, HumanPlayer
from ui import HUD, Board, PygameUI


class App:
    def __init__(self):

        self.game_manager = GameManager(self)
        self.gui = PygameUI(self)
        self.players = []

        self.game_manager.join_room(self.gui)

    def notify(self, sender, event, **kwargs):
        if event == "StartGame":
            # define the params for the game
            formation = kwargs["config"]["formation"][0][1]
            game_type = kwargs["config"]["game_type"][0][1]
            self.game_manager.game_type = game_type

            # make the correct players depending on the config
            player_color = kwargs["config"]["player_color"][0][1]
            self.players = self.initialize_players(game_type, player_color)

            self.game_manager.start_game(formation)
            self.gui.update(self.game_manager)

            # if the first player to move is a cpu make the move
            self.gui.run_game()
        if event == "AiMakeMove":
            player = self.players[0] if self.players[0].color == self.game_manager.current_player_to_move else self.players[1]
            if type(player) == AbaloneAgent:
                # trigger the agent to make a move
                move, time_stamp = player.generate_move(self.game_manager)
                player.make_move(self.game_manager,
                                 player.color, move, time_stamp=time_stamp)
                self.gui.start_button_clicked = True
            self.gui.waiting_for_player_input = True

        if event == "PlayerMakeMove":
            first_marble = kwargs["first_marble"]
            second_marble = kwargs["second_marble"]
            direction = kwargs["direction"]
            time_stamp = 1
            move = Move(first_marble, second_marble, direction,
                        self.game_manager.current_player_to_move)
            # either here or in commit move we want to do isvalidmove(move)
            # if move not valid then set the state of the player event handler back to waiting for first marble
            # if is valid make move and prompt ai to make move
            player = self.players[0] if self.players[0].color == self.game_manager.current_player_to_move else self.players[1]
            self.game_manager.commit_move(
                move=move, player=move.marble, timestamp=time_stamp)
            self.notify(self, "AiMakeMove")
        if event == "IsMarblePlayerToMove":
            # check what marble color is at the marble_pos
            marble_row, marble_col = kwargs["marble_pos"]
            return self.game_manager.get_board()[marble_row][marble_col] == self.game_manager.current_player_to_move

        if event == "getRecordHistory":
            return self.game_manager.get_record_history()

        if event == "UndoLastMove":
            self.game_manager.undo_last_move()

        if event == "GetScore":
            return self.game_manager.game_score

    def initialize_players(self, game_type: GameType, player_color: Marble):
        if game_type == GameType.CPU_VS_CPU:
            return [AbaloneAgent(10, 100, Marble.BLACK), AbaloneAgent(10, 100, Marble.WHITE)]
        elif game_type == GameType.PLAYER_VS_CPU:
            if player_color == Marble.BLACK:
                return [HumanPlayer(10, 100, Marble.BLACK), AbaloneAgent(10, 100, Marble.WHITE)]
            else:
                return [AbaloneAgent(10, 100, Marble.BLACK), HumanPlayer(10, 100, Marble.WHITE)]
        elif game_type == GameType.PLAYER_VS_PLAYER:
            return [HumanPlayer(10, 100, Marble.BLACK), HumanPlayer(10, 100, Marble.WHITE)]

    def run(self):
        self.gui.run()
