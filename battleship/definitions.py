from enum import Enum


class PlayerType(Enum):
    """
    Enum listing all available/expected player types.
    """

    SHIP = 1


class Status(Enum):
    """
    Enum listing all available/expected player status.
    """

    LIVE = 1
    DEAD = 2
