from enum import Enum


class DrawingState(Enum):
    RUNNING = 1
    FINISHED = 2
    PAUSED = 3
    INTERRUPTED = 4
