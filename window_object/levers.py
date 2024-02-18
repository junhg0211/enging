from pygame import Color, Surface, draw
from pygame.constants import BUTTON_LEFT

from window_handler import MouseHandler
from window_object import Object


class Slider(Object):
    BACKGROUND_COLOR = Color(0xA0, 0xA0, 0xA0)
    HANDLE_COLOR = Color(0x20, 0x20, 0x20)

    BACKGROUND_HALF_WIDTH = 10
    HANDLE_HALF_WIDTH = 50
    HANDLE_HALF_HEIGHT = 30

    def __init__(self, x: int, up_y: int, length: int, levels: int, mouse_handler: MouseHandler):
        self.x = x
        self.y = up_y
        self.length = length
        self.max_level = levels - 1
        self.mouse_handler = mouse_handler

        self.value = 0
        self.slider_y = self.get_slider_y()

    def get_slider_y(self) -> float:
        return self.y + self.value / self.max_level * self.length

    def tick(self):
        # check mouse pressed
        if self.mouse_handler.is_pressed(BUTTON_LEFT):
            # check cursor in area
            if self.x - Slider.HANDLE_HALF_WIDTH < self.mouse_handler.x < self.x + Slider.HANDLE_HALF_WIDTH \
                    and self.y < self.mouse_handler.y < self.y + self.length:
                # calculate value
                self.value = round((self.mouse_handler.y - self.y) / self.length * self.max_level)

                # change slider y value
                self.slider_y = self.get_slider_y()

    def render(self, window: Surface):
        # slider background
        draw.rect(
            window, Slider.BACKGROUND_COLOR,
            (self.x - Slider.BACKGROUND_HALF_WIDTH, self.y, Slider.BACKGROUND_HALF_WIDTH * 2, self.length)
        )

        # slider handle
        draw.rect(
            window, Slider.HANDLE_COLOR,
            (self.x - Slider.HANDLE_HALF_WIDTH, self.slider_y - Slider.HANDLE_HALF_HEIGHT,
             Slider.HANDLE_HALF_WIDTH * 2, Slider.HANDLE_HALF_HEIGHT * 2)
        )

    def get_value(self) -> int:
        return self.value


class ReturnSlider(Slider):
    def __init__(self, x: int, up_y: int, length: int, levels: int, return_value: int, mouse_handler: MouseHandler):
        super().__init__(x, up_y, length, levels, mouse_handler)

        self.return_value = return_value

    def tick(self):
        super().tick()

        if not self.mouse_handler.is_pressed(BUTTON_LEFT):
            self.value = self.return_value
            self.slider_y = self.get_slider_y()
