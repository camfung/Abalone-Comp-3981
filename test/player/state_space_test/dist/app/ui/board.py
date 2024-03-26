import pygame
from app.api.enums import Marble
from app.ui.pi_handler import PlayerInputHandler

from app.ui.ui_components import Drawable, EventHandler


class Board(Drawable, EventHandler):
    """
    A class representing the game board, responsible for drawing the board and handling events related to it.
    It implements the Drawable and EventHandler interfaces for graphical display and event handling, respectively.
    """

    CELL_SIZE = 76
    SIDE_MARGIN = 13
    TOP_OFFSET = 100
    TOP_MARGIN = 2
    OFFSET = CELL_SIZE / 2 + SIDE_MARGIN - 5
    ALIGNMENT = [0, -2, -1, -1, 0, 0, 1, 1, 2, 2, 0]

    def __init__(self, callbacks) -> None:
        """
        Initializes the Board class with callback functions for handling game inputs.

        Parameters:
        - callbacks: A tuple or list containing callback functions to handle various player actions.
        """
        super().__init__()
        self.waiting_for_player_input = False
        self.input_handler = PlayerInputHandler(callbacks)

    def handle_event(self, event):
        """
        Handles user input events, specifically mouse button presses for selecting marbles or resetting the game state.

        Parameters:
        - event: The event to be handled, usually a mouse event from the pygame event queue.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            # handle input for players turn
            if self.waiting_for_player_input:
                row, col = Board.get_cell(pos)
                # left click
                if event.button == 1:
                    if row is not None and col is not None:
                        self.input_handler.on_marble_click((row, col))
                # right click
                elif event.button == 3:
                    self.input_handler.reset_state()

    def clicked_marbles(self, first_ball, second_ball):
        row1, col1 = first_ball
        row2, col2 = second_ball

        returned_array = []

        # Check if positions are in the same row
        if row1 == row2:
            new_ball = [(row1, col)
                        for col in range(min(col1, col2) + 1, max(col1, col2))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # Check if positions are in the same column
        if col1 == col2:
            new_ball = [(row, col1)
                        for row in range(min(row1, row2) + 1, max(row1, row2))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # Check if positions are in the same diagonal
        if abs(row1 - row2) == abs(col1 - col2):
            # Determine the direction of the diagonal
            row_step = 1 if row1 < row2 else -1
            col_step = 1 if col1 < col2 else -1

            # Collect locations in the diagonal
            new_ball = [(row, col) for row, col in zip(range(row1 + row_step, row2, row_step),
                                                       range(col1 + col_step, col2, col_step))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # No straight line found
        return []

    def draw(self, surface, game_manager):
        """
        Draws the game board, including the background and marbles, onto the specified surface.

        Parameters:
        - surface: The pygame Surface object where the board should be drawn.
        - game_manager: An instance of the GameManager class, used to access the current state of the game board.
        """
        game_manager = game_manager.get_board()
        clicks = []

        screen = surface
        pygame.display.set_caption("Abalone Board")

        if self.input_handler.first_marble is not None:
            if self.input_handler.second_marble is not None:
                clicks = self.clicked_marbles(
                    self.input_handler.first_marble, self.input_handler.second_marble)
            else:
                clicks.append(self.input_handler.first_marble)
        else:
            clicks = []

        background_image = pygame.image.load(
            "./app/images/Numbered_Board.png", "rb")
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        screen.blit(background_image, (0, self.TOP_OFFSET))

        for row in range(len(game_manager)):
            for col in range(len(game_manager[row])):
                if game_manager[row][col] == Marble.BLACK:
                    if (row, col) in clicks:
                        ball_image = pygame.image.load(
                            "./app/images/dark_black_ball.png")
                    else:
                        ball_image = pygame.image.load(
                            "./app/images/black_ball.png")
                elif game_manager[row][col] == Marble.WHITE:
                    if (row, col) in clicks:
                        ball_image = pygame.image.load(
                            "./app/images/dark_white_ball.png")
                    else:
                        ball_image = pygame.image.load(
                            "./app/images/white_ball.png")
                else:
                    continue

                # Calculate the offset
                # Apply offset to odd rows for Abalone layout
                offset = self.OFFSET if row % 2 == 0 else 0
                total_grid_width = len(
                    game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.SIDE_MARGIN
                total_grid_height = len(
                    game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + \
                    (self.ALIGNMENT[row] + col) * \
                    (self.CELL_SIZE + self.SIDE_MARGIN) - offset
                cell_y = start_y + row * \
                    (self.CELL_SIZE + self.TOP_MARGIN) + self.TOP_OFFSET
                screen.blit(ball_image, (cell_x, cell_y))

    @classmethod
    def get_cell(cls, pos):
        """
        Calculates which cell of the board is at a given pixel position.

        Parameters:
        - pos: A tuple containing the (x, y) coordinates of the pixel position.

        Returns:
        - A tuple (row, col) indicating the cell's row and column.
        Returns (None, None) if the position is outside any cell.
        """
        board = cls.ALIGNMENT
        for row in range(len(board)):
            for col in range(len(board)):
                # Calculate the offset
                # Apply offset to odd rows for Abalone layout
                offset = cls.OFFSET if row % 2 == 0 else 0
                total_grid_width = len(
                    board) * cls.CELL_SIZE + (len(board) - 1) * cls.SIDE_MARGIN
                total_grid_height = len(
                    board) * cls.CELL_SIZE + (len(board) - 1) * cls.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + \
                    (cls.ALIGNMENT[row] + col) * \
                    (cls.CELL_SIZE + cls.SIDE_MARGIN) - offset
                cell_y = start_y + row * \
                    (cls.CELL_SIZE + cls.TOP_MARGIN) + cls.TOP_OFFSET
                rect = pygame.Rect(
                    cell_x,
                    cell_y,
                    cls.CELL_SIZE,
                    cls.CELL_SIZE
                )
                if rect.collidepoint(pos):
                    return row, col
        return None, None
