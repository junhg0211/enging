import pygame
from pygame.event import Event


class Handler:
    def handle(self, event: Event):
        pass

    def tick(self):
        pass


class MouseHandler(Handler):
    def __init__(self):
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

        self.buttons = set()

    def handle(self, event: Event):
        if event.type == pygame.MOUSEMOTION:
            self.x, self.y = event.pos
            self.dx, self.dy = event.rel
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.buttons.add(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.buttons -= {event.button}


class KeyboardHandler(Handler):
    def __init__(self):
        self.keys = set()

    def is_pressed(self, key: int):
        return key in self.keys

    def handle(self, event: Event):
        if event.type == pygame.KEYDOWN:
            self.keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys -= {event.key}
