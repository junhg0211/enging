import pygame

pygame.init()


class Window:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.running = True

        pygame.display.set_caption('Enging')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def tick(self):
        pass

    def render(self):
        # background color
        self.window.fill((255, 255, 255), [(0, 0), (self.width, self.height)])

        # update screen
        pygame.display.update()

    def start(self):
        while self.running:
            self.handle_events()
            self.tick()
            self.render()
