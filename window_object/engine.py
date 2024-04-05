from collections import deque
from math import pi, sin
from random import random
from threading import Thread

from pyaudio import PyAudio, paInt16
from pygame import Surface, Color, draw
from pygame.font import Font

from window_handler import MouseHandler
from window_object import Object
from window_object.display import Display
from window_object.levers import Slider


def separate(number: int, count: int) -> list:
    result = list()

    for _ in range(count):
        number, mod = divmod(number, 256)
        result.append(mod)

    return result


def square(x: float, r: float) -> float:
    if x % (2 * pi) < 2 * pi * r:
        return 1.0
    else:
        return -1.0


def sawtooth(x: float):
    return x / pi % 2 - 1


def pwm(x: float, multiplier: int) -> float:
    if sin(x) > sawtooth(multiplier * x):
        return 1.0
    else:
        return -1.0


class Engine(Object):
    def __init__(self, mouse_handler: MouseHandler):
        self.mouse_handler = mouse_handler

        audio = PyAudio()
        sample_rate = audio.get_default_output_device_info().get("defaultSampleRate")
        assert sample_rate is not None
        self.sample_rate = int(sample_rate)
        self.channels = 1
        self.bitrate = 16
        self.stream = audio.open(
            format=paInt16,
            channels=self.channels,
            input=False,
            output=True,
            rate=self.sample_rate,
        )

        self.volume = 0.0
        self.frequency = 0.0
        self.x = 0.0
        self.pwm_rate = 0
        self.acceleration = 0
        self.enable_rate = 0.0

        self.volume_slider = Slider(100, 100, 400, 100, self.mouse_handler)
        self.pwm_rate_slider = Slider(250, 100, 400, 10, self.mouse_handler)
        self.acceleration_slider = Slider(400, 100, 400, 13, self.mouse_handler)
        self.enable_slider = Slider(550, 100, 400, 12, self.mouse_handler)

        font = Font("./res/font/PretendardJP-Regular.otf", 18)
        black = Color(0, 0, 0)
        white = Color(255, 255, 255)
        self.volume_display = Display(100, 600, 100, 50, font, black, white)
        self.pwm_display = Display(250, 600, 100, 50, font, black, white)
        self.acceleration_display = Display(400, 600, 100, 50, font, black, white)
        self.enable_display = Display(550, 600, 100, 50, font, black, white)

        self.frequency_display = Display(700, 600, 100, 50, font, black, white)

        self.writing = True
        self.thread = Thread(target=self.write_wave)

        self.value = 0
        self.value_history = deque()
        self.value_history_count = 250

        self.thread.start()

    def tick(self):
        self.volume_slider.tick()
        self.pwm_rate_slider.tick()
        self.acceleration_slider.tick()
        self.enable_slider.tick()

        self.volume = self.volume_slider.get_value_rate()
        self.pwm_rate = round(1.5 ** (self.pwm_rate_slider.get_value() + 2))
        self.acceleration = self.acceleration_slider.get_value() - 7
        self.enable_rate = self.enable_slider.get_value_rate()

        self.volume_display.set_text(format(self.volume * 100, ".2f"))
        self.pwm_display.set_text(str(self.pwm_rate))
        self.acceleration_display.set_text(str(self.acceleration))
        self.enable_display.set_text(format(self.enable_rate, ".3f"))

        self.frequency_display.set_text(format(self.frequency, ",.1f"))

        self.volume_display.tick()
        self.pwm_display.tick()
        self.acceleration_display.tick()
        self.enable_display.tick()
        self.frequency_display.tick()

        if self.frequency * self.pwm_rate > 300:
            self.pwm_rate_slider.set_value(self.pwm_rate_slider.get_value() - 1)
        elif self.frequency * self.pwm_rate < 150:
            self.pwm_rate_slider.set_value(self.pwm_rate_slider.get_value() + 1)

        try:
            self.value_history_count = round(self.sample_rate / self.frequency)
        except ZeroDivisionError:
            self.value_history_count = 1
        else:
            if self.value_history_count > 800:
                self.value_history_count = 800

    def render(self, window: Surface):
        self.volume_slider.render(window)
        self.pwm_rate_slider.render(window)
        self.acceleration_slider.render(window)
        self.enable_slider.render(window)

        self.volume_display.render(window)
        self.pwm_display.render(window)
        self.acceleration_display.render(window)
        self.enable_display.render(window)
        self.frequency_display.render(window)

        for i in range(len(self.value_history) - 1):
            history = self.value_history[i]
            try:
                next_history = self.value_history[i + 1]
            except IndexError:
                break
            if self.value_history_count != 0:
                draw.line(
                    window,
                    (0, 0, 0),
                    (700 + i / self.value_history_count * 500, 100 * history + 300),
                    (
                        700 + (i + 1) / self.value_history_count * 500,
                        100 * next_history + 300,
                    ),
                )

    def write_wave(self):
        while self.writing:
            self.frequency += (
                self.acceleration * self.enable_rate - (1 - self.enable_rate) * 2
            ) / self.sample_rate

            if self.frequency < 0.0:
                self.frequency = 0.0

            self.x += 2 * pi * self.frequency / self.sample_rate
            self.x %= 2 * pi
            self.value = pwm(self.x, self.pwm_rate)

            self.value_history.append(self.value)
            while len(self.value_history) > 2 * self.value_history_count:
                for _ in range(self.value_history_count):
                    self.value_history.popleft()

            self.value = self.value * self.enable_rate + sin(self.x) * (
                1 - self.enable_rate
            )
            self.value = self.value * 0.95 + (random() * 2 - 1) * 0.05

            buffer = bytes(
                separate(
                    int(self.value * self.volume / 2 * 2**self.bitrate),
                    self.bitrate // 8,
                )
            )

            try:
                self.stream.write(buffer)
            except OSError:
                self.close()

    def close(self):
        if self.writing:
            self.writing = False
            self.stream.close()
