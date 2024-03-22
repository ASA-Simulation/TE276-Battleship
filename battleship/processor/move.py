from math import cos, radians, sin

import esper

from battleship.component import Action, Health, Position
from battleship.resource import TimeResource
from battleship.utils import Status, normalize

from . import AbstractProcessor


class MoveProcessor(AbstractProcessor):
    """
    Processor that computes the movement/dynamics.

    :param velocity: constant velocity to be applied measured in m/s
    :param damage_rate: max turn rate (control saturation) measured in deg/s
    """

    def __init__(self, velocity: float, turn_rate: float):
        self.vel = velocity  # in m/s
        self.turn_rate = radians(turn_rate)  # in rad/s

    def process(self) -> bool:
        dt = TimeResource().get_dt()

        for _, (position, action, health) in esper.get_components(
            Position, Action, Health
        ):
            #
            # Iterate over all ships (position + action + health)
            #

            if health.status != Status.LIVE:
                # if not alive, skip it
                continue

            desired_heading = action.desired_heading  # in [-pi, +pi]
            current_heading = position.theta  # in [-pi, +pi]

            #
            # Simulate (very simple) control system
            #

            saturation = self.turn_rate * dt  # in [-pi, +pi]

            if abs(normalize(desired_heading - current_heading)) < saturation:
                position.theta = desired_heading
            elif normalize(desired_heading - current_heading) > 0:
                position.theta = normalize(position.theta + saturation)
            else:
                position.theta = normalize(position.theta - saturation)

            #
            # Apply dynamics to postion
            #

            position.y += self.vel * dt * sin(position.theta)
            position.x += self.vel * dt * cos(position.theta)

        return True
