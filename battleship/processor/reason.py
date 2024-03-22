import esper

from battleship.component import Hazard, Position, Route, Tag
from battleship.config import logger
from battleship.definitions import PlayerType
from battleship.path_planning import plan_action
from battleship.utils import get_distance

from . import AbstractProcessor

_logger = logger.getChild(__name__)


class ReasonProcessor(AbstractProcessor):
    """
    Processor that performs the agent's reasoning.
    """

    def process(self) -> bool:
        for entity, tag in esper.get_component(Tag):
            #
            # Iterate over all tagged entites (tag)
            #

            if tag.type != PlayerType.SHIP:
                # There could be more types of players
                # so we should skip them nevertheless
                continue

            # we expect ship agents to have a position and route (through factory)
            position = esper.component_for_entity(entity, Position)
            route = esper.component_for_entity(entity, Route)

            if route.idx == len(route.points):
                # we have already reached our goal somehow
                # it's been a long journey
                return False

            if get_distance(route.points[route.idx], position) < 10:
                # if the agent is near enough (10m)
                # go to the next point in route
                route.idx += 1

                if route.idx == len(route.points):
                    # we have just reached our goal
                    # it's been a long journey
                    _logger.info("Mission accomplished!")
                    return False
                else:
                    _logger.info(
                        f"Changing target to id={route.idx} x={route.points[route.idx].x} y={route.points[route.idx].y}"
                    )

            #
            # Computing desired heading using path planning module
            #

            # collect all hazards
            hazards = [
                (hazard, position)
                for _, (hazard, position) in esper.get_components(Hazard, Position)
            ]

            # compute action
            action = plan_action(
                current_position=position,
                target_position=route.points[route.idx],
                hazards=hazards,
            )

            # dynamically add action to agent (for MoveProcessor)
            esper.add_component(entity, action)

        return True
