from abc import ABC, abstractmethod
import pygame
import pygame_menu
from enums import Formation, UIState
from records import RecordHistory

"""
Essentially what this interface is meant to do is replace the event handling in the pygameUI main game loop. 
The idea is that in the main game loop the handle event will be called on every event for all the ui components. 
The behavior for the events will be defined in the concrete class
"""


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface):
        pass


class HUD(Drawable, EventHandler):
    HUD_WIDTH = 1000
    HUD_HEIGHT = 150
    SCREEN_HEIGHT = 1000

    def __init__(self):
        self.theme = pygame_menu.themes.THEME_DARK
        self.theme.widget_width = 100
        self.ui_instance = PygameUI()

    def handle_event(self, event):
        pass

    def draw(self, surface):
        menu = pygame_menu.Menu("Abalone", self.HUD_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        menu.add.button("Stop Game", pygame_menu.events.EXIT, align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Pause", align=pygame_menu.locals.ALIGN_CENTER) #TODO implementation
        menu.add.button("Reset", self.ui_instance.play_menu, align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Undo Last Move", align=pygame_menu.locals.ALIGN_CENTER) #TODO implementation
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.clock(font_size=25, font_name=pygame_menu.font.FONT_DIGITAL)

        menu.mainloop(surface)

        # TODO Timer
        # TODO Score


class Board(Drawable, EventHandler):
    def handle_event(self, event):
        pass

    def draw(self, surface):
        # Example for drawing to the screen
        # pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(170, 10, 150, 100))
        pass


class UI(ABC):
    drawable_elements = []
    event_handlers = []

    # displays the board and the hud
    @abstractmethod
    def update(self):
        pass


class PygameUI(UI):
    _instance = None
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.theme = pygame_menu.themes.THEME_DARK
        self.screen = pygame.display.set_mode((1000, 1000))
        self.state = UIState.MAIN_MENU
        self.state_actions = {
            UIState.GAME_PLAY: self.run_game,
            UIState.MAIN_MENU: self.main_menu,
            UIState.SETTINGS_MENU: self.settings_menu,
            UIState.PLAY_MENU: self.play_menu,
        }

    def start_the_game(self, config):
        # Placeholder for starting the game with the selected configuration
        print(f"Starting game with config: {config}")
        self.run_game()

    def run_game(self):
        while True:
            self.update()
            for event in pygame.event.get():
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    pos = pygame.mouse.get_pos()

                    # left click
                    if event.button == 1:
                        print(f'Left click at {pos}')

                    # right click
                    elif event.button == 3:
                        print(f'Right click at {pos}')

    def run(self):
        pygame.init()
        action = self.state_actions.get(self.state)
        if action:
            action()
        else:
            # Handle unknown state or default action
            print("Unknown state or default action")

    def update(self):
        self.screen.fill((0, 0, 0))

        for element in self.drawable_elements:
            element.draw(self.screen)

        pygame.display.flip()

    # In these methods we update the state in the board and the Hud and the changes are reflected by the update method
    def update_screen(self, game_state):
        pass

    def display_score(self, game_manager):
        pass

    def display_moves(self, record):
        pass

    def display_time_per_move(self, record):
        pass

    def display_board(self, gameManager):
        pass

    def main_menu(self):
        menu = pygame_menu.Menu('Welcome', PygameUI.SCREEN_WIDTH, PygameUI.SCREEN_HEIGHT,
                                theme=self.theme)

        menu.add.button('Play', self.play_menu)
        menu.add.button('Settings', self.settings_menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    def update_play_button(self, *args):
        print(args)
        # Logic to activate the play button based on selections
        pass

    def play_menu(self):
        menu = pygame_menu.Menu(
            'Play', PygameUI.SCREEN_WIDTH, PygameUI.SCREEN_HEIGHT, theme=self.theme)
        opponent_type = menu.add.selector(
            'Opponent: ', [('Human', 1), ('CPU', 2), ('CPU vs CPU', 3)])
        cpu_level = menu.add.dropselect('CPU Level: ', [(
            'Easy', 1), ('Medium', 2), ('Hard', 3)], default=1, onchange=self.update_play_button)
        formation = menu.add.dropselect('Formation: ', [(
            f.name, f) for f in Formation], default=0, onchange=self.update_play_button)

        menu.add.button('Play', lambda: self.start_the_game({'opponent_type': opponent_type.get_value(),
                                                             'cpu_level': cpu_level.get_value(),
                                                             'formation': formation.get_value()}))

        menu.add.button('Back', self.main_menu)
        menu.mainloop(self.screen)

    def settings_menu(self):
        menu = pygame_menu.Menu('Settings', self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
                                theme=self.theme)

        # Settings options will go here

        menu.add.button('Back', self.main_menu)
        menu.mainloop(self.screen)

    def display_move_history(self):
        menu = pygame_menu.Menu("Move History", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, theme=self.theme)
        table = menu.add.table(table_id='records_table', font_size=20, font_color="Black")
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Turn #', 'White Moves', 'Black Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        # Hardcoded for now
        records = ["Example move"]

        # Modify this to match formatting of record history
        for index, record in enumerate(records, start=1):
            table.add_row([index-1, record, record])

        menu.add.button('Back', self.run_game)
        menu.mainloop(self.screen)
