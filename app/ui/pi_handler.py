import time

from app.api.enums import *


class PlayerInputHandler:
    def __init__(self, callbacks):
        """
        Initialize the game input handler with specific callbacks.

        Parameters:
        - callbacks (tuple): A tuple containing two functions, execute_move and is_marble_player_to_move,
          used to handle game logic and check if a marble belongs to the player making the move.
        """

        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None
        self.start_time = 0
        self.execute_move, self.is_marble_player_to_move, self.update_board = callbacks

    def on_marble_click(self, marble_position):
        """
        Handle marble click events based on the current state of the game.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
        # print("initial state: ", str(self))

        # first marble click
        if self.state == PlayerInputEvents.AWAITING_FIRST_MARBLE:
            self.__on_awaiting_first_marble(marble_position)

        # second marble click
        elif self.state == PlayerInputEvents.AWAITING_SECOND_MARBLE:
            self.__on_awaiting_second_marble(marble_position)

        # direction clicked for more than 1 marble move
        elif self.state == PlayerInputEvents.AWAITING_DIRECTION:
            self.__on_awaiting_direction(marble_position)
        print("final state: ", str(self))

    def __on_awaiting_first_marble(self, marble_position):
        """
        Handle the event when awaiting the first marble selection.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
        else:
            # do nothing
            pass

    def __on_awaiting_second_marble(self, marble_position):
        """
        Handle the event when awaiting the second marble selection.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
        # print("second marble clicked")
        # clicked first_marble
        # so deselected it go back to awaiting first marble
        if self.first_marble == marble_position:
            self.first_marble = None
            self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE

        elif self.is_adjacent(self.first_marble, marble_position):

            # Here we handle a single marble move
            if self.is_valid_direction(self.first_marble, marble_position):
                self.second_marble = self.first_marble
                direction = self.calculate_direction(
                    self.first_marble, marble_position)
                self.execute_move(self.first_marble,
                                  self.second_marble, direction, (time.time() - self.start_time))
                self.reset_state()

            # handle second marble selected
            self.second_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_DIRECTION

    def __on_awaiting_direction(self, marble_position):
        """
        Handle the event when awaiting the direction selection after selecting two marbles.

        Parameters:
        - marble_position (tuple): The position of the direction or third marble clicked.
        """
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.second_marble = None
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
        else:
            direction = self.calculate_direction(
                self.second_marble, marble_position)
            if self.is_valid_direction(self.second_marble, marble_position):
                self.execute_move(self.first_marble,
                                  self.second_marble, direction, (time.time() - self.start_time))
                self.reset_state()
            else:
                # not a valid direction
                return

    def __str__(self):
        """
        Returns a string representation of the current game state.

        Returns:
        - str: A string representation of the current game state.
        """
        return f'{self.state}, First: {self.first_marble}, Second: {self.second_marble}'

    # checks if second position is within dist of first position
    def is_adjacent(self, first_position, second_position, dist=2):
        """
        Check if two positions are adjacent based on a specified distance.

        Parameters:
        - first_position (tuple): The first position.
        - second_position (tuple): The second position.
        - dist (int): The maximum distance for two positions to be considered adjacent.

        Returns:
        - bool: True if the positions are adjacent, False otherwise.
        """
        # Calculate row and column differences
        row_diff = abs(first_position[0] - second_position[0])
        col_diff = abs(first_position[1] - second_position[1])

        # Adjacency logic for a hexagonal grid
        if row_diff > dist or col_diff > dist:
            return False
        return True

    # checks if the to position is adjacent and not occupied
    def is_valid_direction(self, from_position, to_position):
        """
        Check if moving from one position to another is a valid direction and not occupied by the player's own marble.

        Parameters:
        - from_position (tuple): The starting position.
        - to_position (tuple): The target position.

        Returns:
        - bool/None: True if the direction is valid, False or None otherwise.
        """

        # check if occupied by your own
        if self.is_marble_player_to_move(to_position):
            return False

        # Reuse is_adjacent logic for direction validity
        return self.is_adjacent(from_position, to_position, 1)

    def calculate_direction(self, from_position, to_position):
        """
        Calculate the direction of movement from one position to another.

        Parameters:
        - from_position (tuple): The starting position.
        - to_position (tuple): The target position.

        Returns:
        - Direction: The direction of movement.
        """
        # Direction is calculated based on row and column differences
        row_diff = to_position[0] - from_position[0]
        col_diff = to_position[1] - from_position[1]

        # Mapping differences to directions based on the Direction enum
        if row_diff == -1 and col_diff == 0:
            return Direction.UP_LEFT
        elif row_diff == -1 and col_diff == 1:
            return Direction.UP_RIGHT
        elif row_diff == 0 and col_diff == 1:
            return Direction.RIGHT
        elif row_diff == 1 and col_diff == 0:
            return Direction.DOWN_RIGHT
        elif row_diff == 1 and col_diff == -1:
            return Direction.DOWN_LEFT
        elif row_diff == 0 and col_diff == -1:
            return Direction.LEFT
        else:
            return None  # Invalid direction or positions are not adjacent

    def reset_state(self):
        """
        Reset the game state to its initial conditions, awaiting the first marble selection.
        """
        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None
