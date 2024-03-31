import datetime
import threading
import time

from app.api.enums import GameType, Marble, AgentType
from app.gameplay.move import Move

from app.communication.game_manager import GameManager

from app.players.agent import AbaloneAgent
from app.players.test_agents.random_agent import RandomAgent
from app.players.human import HumanPlayer
from app.players.test_agents.callum import AgentCallum
from app.players.test_agents.cameron import AgentCameron
from app.players.test_agents.elsa import AgentElsa
from app.players.test_agents.joey import AgentJoey

from app.ui.ui import PygameUI
from app.gameplay.timer import Timer


class App:
    """
    The main application class that orchestrates the game by
    integrating the game manager, user interface (UI), and players.
    It handles events and notifications across these components to manage game flow and state.
    """

    def __init__(self):
        """
        Initializes the application, setting up the game manager, UI, and player list.
        It also registers the UI with the game manager for updates.
        """
        self.game_manager = GameManager(self)
        self.gui = PygameUI(self)
        self.players = []
        self.timer = Timer()

        self.game_manager.join_room(self.gui)

    def notify(self, sender, event, **kwargs):
        thread = threading.Thread(
            target=self.notify, args=(self, "ThreadedAiMakeMove"))
        """
        Handles notifications sent from different parts of the application,
        acting upon various events like starting the game, making moves, undoing moves, and querying game state.

        Parameters:
        - sender: The component that sent the notification.
        - event: A string representing the type of event that occurred.
        - **kwargs: Additional keyword arguments providing context and data needed to handle the event.
        """
        if event == "StartGame":
            """
            Starts a new game with the specified configuration. 
            This event initializes players, sets up the game board, and starts the game loop.

            Parameters:
            - config: A dictionary containing the game configuration such as formation, game type, and player color.
            """

            # define the params for the game
            formation = kwargs["config"]["formation"][0][1]
            game_type = kwargs["config"]["game_type"][0][1]
            self.game_manager.game_type = game_type

            # make the correct players depending on the config
            player_color = kwargs["config"]["player_color"][0][1]
            move_limit = kwargs["config"]["move_limit"]

            black_time_limit = kwargs["config"]["black_time_limit"]
            white_time_limit = kwargs["config"]["white_time_limit"]
            agent_level = kwargs["config"]["agent_level"][0][1]

            self.timer._white_turn_time_limit = white_time_limit
            self.timer._black_turn_time_limit = black_time_limit
            self.players = self.initialize_players(
                game_type, player_color, move_limit, black_time_limit, white_time_limit, agent_level)

            self.game_manager.start_game(formation)
            self.gui.update(self.game_manager)

            # if the first player to move is an agent make the move
            self.gui.run_game()
        if event == "AiMakeMove":
            """
            Triggers the AI agent to calculate and make a move. This event is called when it's the AI's turn to play.

            No specific parameters are required for this event 
            as the AI's decision-making process is internal and based on the current game state.
            """
            thread.start()

        if event == "ThreadedAiMakeMove":
            player = self.players[0] if self.players[0].color == self.game_manager.current_player_to_move else \
                self.players[1]
            if isinstance(player, AbaloneAgent):
                # trigger the agent to make a move
                move, time_stamp = player.generate_move(
                    self.game_manager, self.timer)
                if self.timer._game_started:
                    player.make_move(self.game_manager,
                                     player.color, move, timestamp=time_stamp)
                    self.gui.start_button_clicked = True
            if thread.is_alive():
                thread.join()
            if not self.timer.paused:
                self.timer.current_turn_start_time = time.time()
                self.timer._elapsed_time = time.time()
            self.timer.paused = False
            self.gui.waiting_for_player_input = True

        if event == "PlayerMakeMove":
            """
            Processes a move made by a player. This includes validating the move, updating the game state, 
            and possibly triggering the AI to make its move.

            Parameters:
            - first_marble: The position of the first marble selected by the player.
            - second_marble: The position of the second marble selected by the player (if applicable).
            - direction: The direction in which the player wishes to move the selected marbles.
            """
            first_marble = kwargs["first_marble"]
            second_marble = kwargs["second_marble"]
            direction = kwargs["direction"]
            time_stamp = time.time() - self.timer.current_turn_start_time
            move = Move(first_marble, second_marble, direction,
                        self.game_manager.current_player_to_move)
            # either here or in commit move we want to do is_valid_move(move)
            # if move not valid then set the state of the player event handler back to waiting for first marble
            # if is valid make move and prompt AI to make move
            player = self.players[0] if self.players[0].color == self.game_manager.current_player_to_move else \
                self.players[1]
            start = datetime.datetime.now()
            self.game_manager.commit_move(
                move=move, player=move.marble, timestamp=time_stamp)
            end = datetime.datetime.now()
            print("commit move:", end - start)
            self.timer.current_turn_start_time = time.time()
            self.timer._elapsed_time = time.time()
            self.notify(self, "AiMakeMove")
        if event == "IsMarblePlayerToMove":
            """
            Checks if the marble at a given position belongs to the current player to move.

            Parameters:
            - marble_pos: The board position of the marble to check.

            Returns:
            - A boolean indicating whether the marble at the specified position belongs to the current player.
            """
            # check what marble color is at the marble_pos
            marble_row, marble_col = kwargs["marble_pos"]
            return self.game_manager.get_board()[marble_row][marble_col] == self.game_manager.current_player_to_move

        if event == "getRecordHistory":
            return self.game_manager.get_record_history()

        if event == "UndoLastMove":
            self.game_manager.undo_last_move()

        if event == "GetScore":
            return self.game_manager.game_score

        if event == "StartTimer":
            self.timer.start_timer()

        if event == "ResetTimer":
            self.timer.reset_time()

        if event == "GetTimerValues":
            return self.timer.get_timer_values()

        if event == "UpdateTimer":
            self.timer.update_timer(self.game_manager)

        if event == "ReduceAggregateTime":
            if kwargs["player"] == Marble.BLACK:
                self.timer._black_total_aggregate_time -= kwargs["time"]
                if self.timer._black_total_aggregate_time < 0:
                    self.timer._black_total_aggregate_time = 0
            elif kwargs["player"] == Marble.WHITE:
                self.timer._white_total_aggregate_time -= kwargs["time"]
                if self.timer._white_total_aggregate_time < 0:
                    self.timer._white_total_aggregate_time = 0

        if event == "PauseTimer":
            self.gui.waiting_for_player_input = False
            self.timer.pause_timer()

        # Add pause timer thing here

    def initialize_players(self, game_type: GameType, player_color: Marble, move_limit: int, black_time_limit: int,
                           white_time_limit: int, agent_level: AgentType):
        """
        Initializes players based on the selected game type and player colors.

        Parameters:
        - game_type: An enumeration value of GameType
        indicating whether it's player vs. agent, agent vs. agent, or player vs. player.
        - player_color: An enumeration value of Marble indicating the color chosen by the player.

        Returns:
        A list of initialized player objects for the game.
        """
        if game_type == GameType.AGENT_VS_AGENT:
            return [AbaloneAgent(black_time_limit, move_limit, Marble.BLACK), AbaloneAgent(white_time_limit, move_limit, Marble.WHITE)]

        elif game_type == GameType.PLAYER_VS_AGENT:
            if player_color == Marble.BLACK:
                human_player = HumanPlayer(
                    black_time_limit, move_limit, Marble.BLACK)

                if agent_level == AgentType.ABALONE_AGENT:
                    return [human_player, RandomAgent(white_time_limit, move_limit, Marble.WHITE)]
                elif agent_level == AgentType.RANDOM_AGENT:
                    return [human_player, RandomAgent(white_time_limit, move_limit, Marble.WHITE)]
                elif agent_level == AgentType.AGENT_CAMERON:
                    return [human_player, AgentCameron(white_time_limit, move_limit, Marble.WHITE)]
                elif agent_level == AgentType.AGENT_CALLUM:
                    return [human_player, AgentCallum(white_time_limit, move_limit, Marble.WHITE)]
                elif agent_level == AgentType.AGENT_JOEY:
                    return [human_player, AgentJoey(white_time_limit, move_limit, Marble.WHITE)]
                elif agent_level == AgentType.AGENT_ELSA:
                    return [human_player, AgentElsa(white_time_limit, move_limit, Marble.WHITE)]

            else:
                human_player = HumanPlayer(
                    white_time_limit, move_limit, Marble.WHITE)

                if agent_level == AgentType.ABALONE_AGENT:
                    return [AbaloneAgent(black_time_limit, move_limit, Marble.BLACK), human_player]
                elif agent_level == AgentType.AGENT_CAMERON:
                    return [AgentCameron(black_time_limit, move_limit, Marble.BLACK), human_player]
                elif agent_level == AgentType.AGENT_CALLUM:
                    return [AgentCallum(black_time_limit, move_limit, Marble.BLACK), human_player]
                elif agent_level == AgentType.AGENT_JOEY:
                    return [AgentJoey(black_time_limit, move_limit, Marble.BLACK), human_player]
                elif agent_level == AgentType.AGENT_ELSA:
                    return [AgentElsa(black_time_limit, move_limit, Marble.BLACK), human_player]

        elif game_type == GameType.PLAYER_VS_PLAYER:
            return [HumanPlayer(black_time_limit, move_limit, Marble.BLACK), HumanPlayer(white_time_limit, move_limit, Marble.WHITE)]

    def run(self):
        """
        Starts the application by displaying the main menu and initializing the game loop.
        """
        self.gui.run()

    def reset_board(self):
        self.game_manager.reset_board()
