from math import pi, sin
from threading import Thread

import pyaudio
from window import Window


def separate(number: int, count: int) -> list:
    result = list()

    # if number < 0:
    #     number = (number ^ (1 << (count*8)-1)) + 1
    #     number %= 1 << (count*8)

    for _ in range(count):
        number, mod = divmod(number, 256)
        result.append(mod)

    return result


def square(x: float, r: float) -> float:
    if x % (2*pi) < 2*pi * r:
        return 1.0
    else:
        return -1.0


def sawtooth(x: float):
    return x/pi % 2 - 1


def pwm(x: float, multiplier: float) -> float:
    if sin(x) > sawtooth(multiplier * x):
        return 1.0
    else:
        return -1.0


def write_wave(sample_rate: int, bitrate: int, stream: pyaudio.Stream):
    volume = 0.05
    duration = 2.0
    frequency = 55.0

    for i in range(int(sample_rate * duration)):
        frequency += 30/sample_rate
        x = 2*pi * frequency * (i / sample_rate)
        value = pwm(x, 7 if i < sample_rate else 4)

        buffer = bytes(separate(int(value * volume/2 * 2**bitrate), bitrate//8))

        stream.write(buffer)


def main():
    # -- audio thing
    # initialise audio stream
    audio = pyaudio.PyAudio()
    output_info = audio.get_default_output_device_info()
    sample_rate = int(output_info.get('defaultSampleRate'))
    channels = 1
    bitrate = 16
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        input=False,
        output=True,
        rate=sample_rate
    )

    # write wave to the stream
    thread = Thread(target=write_wave, args=(sample_rate, bitrate, stream))
    thread.start()

    # -- window thing
    window = Window()
    window.start()

    # -- close audio stream
    stream.close()


if __name__ == '__main__':
    main()
