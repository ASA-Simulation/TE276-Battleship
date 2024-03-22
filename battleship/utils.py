from math import atan2, pi, sqrt
import esper

from battleship.component import Health, Position
from battleship.definitions import Status


def normalize(angle: float) -> float:
    aux = angle
    while aux > pi:
        aux -= 2 * pi
    while aux < -pi:
        aux += 2 * pi
    return aux


def get_heading(start: Position, end: Position) -> float:
    """Return the heading from :param start: to :param end: measured in radians."""
    return atan2(end.y - start.y, end.x - start.x)


def get_distance(start: Position, end: Position) -> float:
    """Return the euclidean distance from :param start: to :param end: measured in meters."""
    return sqrt((end.y - start.y) ** 2 + (end.x - start.x) ** 2)


def has_alive() -> bool:
    """Return whether there is any entity left with health status live."""
    has = False
    for _, health in esper.get_component(Health):
        if health.status == Status.LIVE:
            has = True
            break
    return has
