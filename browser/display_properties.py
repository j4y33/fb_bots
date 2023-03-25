import random
from typing import Tuple


class DisplayProperties:

    @classmethod
    def get_size(cls) -> Tuple[int, int]:
        size = [(1600, 900),
                (1366, 768),
                (1920, 1080),
                (1680, 1050),
                (2048, 1152),
                (1280, 1024),
                (1280, 720),
                (1280, 800),
                (1024, 768),
                (800, 600),
                (640, 360)]
        return random.choice(size)