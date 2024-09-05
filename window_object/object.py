from pygame import draw, Surface, Color
from pygame.font import Font


class Object:
    def tick(self):
        pass

    def render(self, window: Surface):
        pass

    def close(self):
        pass


class Rectangle(Object):
    def __init__(self, x: int, y: int, width: int, height: int, color: Color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def render(self, window: Surface):
        draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


class Text(Object):
    def __init__(self, x: int, y: int, text: str, color: Color, font: Font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font

        self.surface: Surface
        self.generate_surface()

    def set_text(self, text: str):
        self.text = text
        self.generate_surface()

    def generate_surface(self):
        self.surface = self.font.render(self.text, True, self.color)

    def render(self, window: Surface):
        window.blit(self.surface, (self.x, self.y))
