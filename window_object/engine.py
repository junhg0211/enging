from math import pi, sin
from threading import Thread

from pyaudio import PyAudio, paInt16
from pygame import Surface

from window_handler import MouseHandler
from window_object import Object
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
        self.sample_rate = int(
            audio
            .get_default_output_device_info()
            .get('defaultSampleRate')
        )
        self.channels = 1
        self.bitrate = 16
        self.stream = audio.open(
            format=paInt16,
            channels=self.channels,
            input=False,
            output=True,
            rate=self.sample_rate
        )

        self.volume = 0.01
        self.frequency = 0.0
        self.x = 0.0
        self.pwm_rate = 7
        self.acceleration = 0

        self.volume_slider = Slider(100, 100, 400, 100, self.mouse_handler)
        self.pwm_rate_slider = Slider(250, 100, 400, 10, self.mouse_handler)
        self.acceleration_slider = Slider(400, 100, 400, 10, self.mouse_handler)

        self.volume_slider.set_value_rate(self.volume)
        self.pwm_rate_slider.set_value(self.pwm_rate)

        self.writing = True
        self.thread = Thread(target=self.write_wave)

        self.thread.start()

    def tick(self):
        self.volume_slider.tick()
        self.pwm_rate_slider.tick()
        self.acceleration_slider.tick()

        self.volume = self.volume_slider.get_value_rate()
        self.pwm_rate = self.pwm_rate_slider.get_value() + 2
        self.acceleration = self.acceleration_slider.get_value() - 6

    def render(self, window: Surface):
        self.volume_slider.render(window)
        self.pwm_rate_slider.render(window)
        self.acceleration_slider.render(window)

    def write_wave(self):
        while self.writing:
            self.frequency += self.acceleration * 2 / self.sample_rate
            if self.frequency < 0.0:
                self.frequency = 0.0

            self.x += 2 * pi * self.frequency / self.sample_rate
            self.x %= 2 * pi
            value = pwm(self.x, self.pwm_rate)

            buffer = bytes(
                separate(
                    int(value * self.volume / 2 * 2 ** self.bitrate),
                    self.bitrate // 8
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
