import pygame_menu
from app.ui.ui_components import Drawable, EventHandler


class HUD(Drawable, EventHandler):
    """
    A Heads-Up Display (HUD) class that handles the creation and management of the game's interface elements.
    It extends both Drawable and EventHandler interfaces to allow for drawing the HUD and handling input events.
    """
    HUD_HEIGHT = 150
    menu = None
    record_menu = None

    def __init__(self, gui, callbacks):
        """
        Initializes the HUD with a reference to the GUI instance and a tuple of callback functions.

        Parameters:
        - gui: An instance of the GUI class, used to access GUI-related attributes and methods.
        - callbacks: A tuple containing references to callback functions for game actions like start, undo, and pause.
        """
        self.ui_instance = gui
        self.theme = self.ui_instance.theme
        self.theme.widget_width = 100
        self.score_label = None
        self._white_balls = 0
        self._black_balls = 0

        self.start_game_cb, self.undo_move_cb, self.pause_game_cb = callbacks

    def create_hud(self):
        """
        Creates the HUD menu with game control buttons like start, stop, pause, reset, undo last move,
        and show move history.

        Returns:
        - menu: A pygame_menu.Menu instance representing the HUD with all the control buttons.
        """
        menu = pygame_menu.Menu("Abalone", self.ui_instance.SCREEN_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        menu.add.button("Start Game", self.start_game_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Stop Game", pygame_menu.events.EXIT,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Pause", self.pause_game_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Reset", self.ui_instance.play_menu,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Undo Last Move", self.undo_move_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)
        self.score_label = menu.add.label(
            f"White Score: {self._white_balls}   Black Score:  {self._black_balls}  ")

        return menu

    @property
    def white_balls(self):
        """
        Property getter for the number of white balls.

        Returns:
        - _white_balls: The current number of white balls.
        """
        return self._white_balls

    @white_balls.setter
    def white_balls(self, value):
        """
        Property setter for the number of white balls. Updates the score label with the new value.

        Parameters:
        - value: The new number of white balls.
        """
        self._white_balls = value
        if self.score_label is not None:
            self.score_label.set_title(
                f"White Score: {self._white_balls}   Black Score: {self._black_balls}  ")

    @property
    def black_balls(self):
        """
        Property getter for the number of black balls.

        Returns:
        - _black_balls: The current number of black balls.
        """
        return self._black_balls

    @black_balls.setter
    def black_balls(self, value):
        """
        Property setter for the number of black balls. Updates the score label with the new value.

        Parameters:
        - value: The new number of black balls.
        """
        self._black_balls = value
        if self.score_label is not None:
            self.score_label.set_title(
                f"White Score: {self._white_balls}   Black Score:  {self._black_balls}  ")

    def get_menu(self):
        """
        Retrieves the HUD menu, creating it if it does not already exist.

        Returns:
        - menu: The pygame_menu.Menu instance representing the HUD.
        """
        if self.menu is None:
            self.menu = self.create_hud()

        return self.menu

    def handle_event(self, event):
        """
        Handles an input event, passing it to the HUD menu for processing.

        Parameters:
        - event: The event to be handled, typically from the pygame event queue.
        """
        menu = self.get_menu()
        menu.update([event])

    def draw(self, surface, game_manager):
        """
        Draws the HUD menu onto the specified surface.

        Parameters:
        - surface: The pygame surface to draw the HUD on.
        - game_manager: The game manager instance, used to access game-related data and methods.
        """
        menu = self.get_menu()
        menu.draw(surface)

        # Record Menu
        record_menu = pygame_menu.Menu(
            "Move History", 300, 850, theme=self.theme, position=(100, 100, True))
        table = record_menu.add.table(table_id='records_table',
                                      font_size=12, font_color="Black")
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        records = self.ui_instance._app.notify(self, "getRecordHistory")

        for index, record in enumerate(records, start=1):
            str_record = str(record)
            table.add_row([str_record])
            print(record)

        record_menu.add.button('Back', self.ui_instance.run_game)  # for testing purposes
        record_menu.draw(surface)
