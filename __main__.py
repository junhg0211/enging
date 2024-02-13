from math import pi, sin

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


def audio_main():
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

    volume = 0.1
    duration = 2.0
    frequency = 440.0
    for i in range(int(sample_rate * duration)):
        x = 2*pi * frequency * (i / sample_rate)
        value = sin(x)

        byte = bytes(separate(int(value * volume/2 * 2**bitrate), bitrate//8))
        stream.write(byte)

    stream.close()


def main():
    window = Window()

    window.start()


if __name__ == '__main__':
    main()
