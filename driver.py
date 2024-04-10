import contextlib

with contextlib.redirect_stdout(None):
    import pygame

with contextlib.redirect_stdout(None):
    import pygame_menu

from app.app import App


def main():
    iconSurface = pygame.image.load('app/images/icon.png')
    pygame.display.set_icon(iconSurface)
    theme = pygame_menu.themes.THEME_DARK
    screen = pygame.display.set_mode(
        (1450, 1000))
    app = App(theme, screen)

    pygame.init()
    app.gui.main_menu()


if __name__ == '__main__':
    main()
