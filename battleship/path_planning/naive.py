from typing import List, Tuple

from battleship.component import Action, Hazard, Position
from battleship.utils import get_heading


def naive(
    current_position: Position,
    target_position: Position,
    _: List[Tuple[Hazard, Position]],
) -> Action:
    """
    Naive solution: approach the target ignoring all hazards.

    :param current_position: the agent's current position
    :param target_position: the agent's target position
    :param _: list of hazard metadata and position (ignored)
    :return: the chosen action
    """
    heading = get_heading(start=current_position, end=target_position)
    return Action(desired_heading=heading)
