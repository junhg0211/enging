from pygame import Color, Surface
from pygame.font import Font

from util import center
from window_object import Object, Text, Rectangle


class Display(Object):
    def __init__(
            self,
            center_x: int, center_y: int,
            width: int, height: int,
            font: Font,
            background_color: Color, color: Color
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.font = font
        self.background_color = background_color
        self.color = color

        self.text = ''

        self.background = Rectangle(
            center(self.center_x, self.width),
            center(self.center_y, self.height),
            self.width, self.height, self.background_color
        )
        self.text_object = Text(
            self.center_x, self.center_y, self.text, self.color, self.font
        )

    def set_text(self, text: str):
        self.text = text

        self.text_object.set_text(self.text)
        self.text_object.x = center(self.center_x, self.text_object.surface.get_width())
        self.text_object.y = center(self.center_y, self.text_object.surface.get_height())

    def tick(self):
        self.background.tick()
        self.text_object.tick()

    def render(self, window: Surface):
        self.background.render(window)
        self.text_object.render(window)
