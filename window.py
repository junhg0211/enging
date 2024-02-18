import pygame

from window_handler import KeyboardHandler, MouseHandler

pygame.init()


class Window:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.running = True

        self.objects = list()

        self.keyboard_handler = KeyboardHandler()
        self.mouse_handler = MouseHandler()

        pygame.display.set_caption('Enging')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.keyboard_handler.handle(event)
            self.mouse_handler.handle(event)

    def tick(self):
        # tick handlers
        self.keyboard_handler.tick()
        self.mouse_handler.tick()

        # tick objects
        for obj in self.objects:
            obj.tick()

    def render(self):
        # background color
        self.window.fill((255, 255, 255), [(0, 0), (self.width, self.height)])

        # render objects
        for obj in self.objects:
            obj.render(self.window)

        # update screen
        pygame.display.update()

    def start(self):
        while self.running:
            self.handle_events()
            self.tick()
            self.render()
