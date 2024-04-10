
from abc import ABC, abstractmethod

import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface, game_manager):
        pass


class Button(Drawable, EventHandler):
    def __init__(self, x, y, width, height, color, highlight_color, text, text_color, font_size, clicked_callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.highlight_color = highlight_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.clicked_callback = clicked_callback

    def draw(self, screen, game_manager):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked_callback()
