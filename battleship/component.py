from dataclasses import dataclass as component
from pathlib import Path
from typing import List, Tuple

from pygame.image import load
from pygame.transform import flip, scale

from battleship.definitions import PlayerType, Status


@component
class Action:
    """
    Action request for the ship.

    :param desired_heading: the desired heading for control systems
    """

    desired_heading: float


@component
class Hazard:
    """
    Hazard metadata.

    :param safe_dist: safe distance to keep in order to avoid damages
    :param damage_rate: the max damage rate inflicted in every step
    """

    safe_dist: float
    damage_rate: float


@component
class Health:
    """
    Player's health/status metadata.

    :param health: amount of health available
    :param status: current status (alive/dead)
    """

    health: float
    status: Status


@component
class Position:
    """
    Player's health/status metadata.

    :param health: amount of health available
    :param status: current status (alive/dead)
    """

    x: float
    y: float
    theta: float


class Renderable:
    """
    Metadata for rendering.

    :param image: filesystem path for the entity's image to be shown
    """

    def __init__(self, image: Path) -> None:
        if not image.suffix.endswith(".png"):
            raise ValueError(
                f"unexpected image file extension: '{image.suffix}', expected '.png'"
            )

        surface = load(image)
        self.image = flip(scale(surface, (24, 24)), flip_x=1, flip_y=0)


class Route:
    """
    A route to be executed by a player.

    :param nav: list of positions (x, y) that make the route
    """

    def __init__(self, nav: List[Tuple[float, float]]) -> None:
        self.points = [Position(x, y, 0) for (x, y) in nav]
        self.idx = 0


@component
class Tag:
    """
    Special metadata tagged to entities/players.

    :param type: the type of player being tagged
    """

    type: PlayerType
