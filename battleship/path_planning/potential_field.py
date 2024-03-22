from math import atan2, cos, pow, sin
from typing import List, Tuple

from battleship.component import Action, Hazard, Position
from battleship.utils import get_distance, get_heading


def potential_field(
    current_position: Position,
    target_position: Position,
    hazards: List[Tuple[Hazard, Position]],
) -> Action:
    """
    Naive solution: approach the target ignoring all hazards.

    :param current_position: the agent's current position
    :param target_position: the agent's target position
    :param hazards: list of hazard metadata and position (tuple with this order)
    :return: the chosen action
    """

    #
    # First, the forces of attraction: in direction of the target position
    #
    towards_target = get_heading(start=current_position, end=target_position)
    weight_attraction = 1.0

    res_x = cos(towards_target) * weight_attraction
    res_y = sin(towards_target) * weight_attraction

    #
    # Then, the forces of repulsion from the hazard sources
    #

    for hazard, position in hazards:
        # exponent used in weighting function
        exp_param = 2.0

        heading = get_heading(start=current_position, end=position)
        dist = get_distance(start=current_position, end=position)
        safe_dist = hazard.safe_dist

        #
        # The computation of the repulsion weight has 3 regions:
        # 1st) from infinity to 2 * safe_dist => 0 (min value)
        # 2nd) from 2 * safe_dist to safe_dist => polynomial from 0 to 1
        # 3rd) from safe_dist to 0m => 1.0 (max value)
        #

        if dist > 2 * safe_dist:
            weight_repulsion = 0.0
        elif dist > safe_dist:
            weight_repulsion = pow((safe_dist * 2.0 - dist), exp_param) / pow(
                (safe_dist), exp_param
            )
        else:
            weight_repulsion = 1.0

        # vetorial sum decomposed in x and y axis
        res_x -= cos(heading) * weight_repulsion
        res_y -= sin(heading) * weight_repulsion

    return Action(desired_heading=atan2(res_y, res_x))
