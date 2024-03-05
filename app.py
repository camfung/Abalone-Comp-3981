from enums import Formation, GameType, Marble
from gameplay import Game
from communication import GameManager
from players import AbaloneAgent, HumanPlayer
from ui import HUD, Board, PygameUI


class App:
    def __init__(self):
        self.game_manager = GameManager(self)
        self.gui = PygameUI(self)
        self.players = []

        hud = HUD()
        board = Board()

        # add the drawables
        self.gui.drawable_elements.append(hud)
        self.gui.drawable_elements.append(board)

        # add the event handlers
        self.gui.event_handlers.append(hud)
        self.gui.event_handlers.append(board)

        self.game_manager.join_room(self.gui)

    def notify(self, sender, event, **kwargs):
        if sender == self.gui:
            if event == "StartGame":
                # define the params for the game
                formation = kwargs["config"]["formation"][0][1]
                game_type = kwargs["config"]["game_type"][0][1]
                self.game_manager.game_type = game_type

                # make the correct players depending on the config
                self.players = self.initialize_players(game_type)

                self.game_manager.start_game(formation)
                self.gui.update(self.game_manager)

                # if the first player to move is a cpu make the move
                self.gui.run_game()
            if event == "MakeFirstMove":
                player = self.players[0] if self.players[0].color == self.game_manager.current_player_to_move else self.players[1]
                if type(player) == AbaloneAgent:
                    # trigger the agent to make a move
                    move = player.generate_move(self.game_manager)
                    player.make_move(self.game_manager, player.color, move)
                    self.gui.start_button_clicked = True
                else:
                    # set a flag in the ui to let it know that we are waiting for a move to be made
                    self.gui.waiting_for_player_input = True

    def initialize_players(self, game_type: GameType):
        if game_type == GameType.CPU_VS_CPU:
            return [AbaloneAgent(10, 100, Marble.BLACK), AbaloneAgent(10, 100, Marble.WHITE)]
        elif game_type == GameType.PLAYER_VS_CPU:
            return [AbaloneAgent(10, 100, Marble.BLACK), HumanPlayer(10, 100, Marble.WHITE)]
        elif game_type == GameType.PLAYER_VS_PLAYER:
            return [HumanPlayer(10, 100, Marble.BLACK), HumanPlayer(10, 100, Marble.WHITE)]

    def run(self):
        self.gui.run()
