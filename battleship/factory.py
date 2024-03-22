from pathlib import Path
from typing import List, Tuple

import esper

from battleship.component import (
    Hazard,
    Health,
    Position,
    Renderable,
    Route,
    Status,
    Tag,
)
from battleship.definitions import PlayerType


def new_ship(x: float, y: float, nav: List[Tuple[float, float]]) -> int:
    """Create a new entity SHIP with all expected components and add to simulation"""
    entity = esper.create_entity()
    esper.add_component(entity, Tag(PlayerType.SHIP))
    esper.add_component(entity, Health(100.0, Status.LIVE))
    esper.add_component(entity, Position(x, y, 0)),
    esper.add_component(entity, Renderable(image=Path("./icons/ship.png")))
    esper.add_component(entity, Route(nav))
    esper.add_component(entity, Health(100.0, Status.LIVE))
    return entity


def new_hazard(lat: float, lon: float, dist: float, rate: float) -> int:
    """Create a new entity HAZARD with all expected components and add to simulation"""
    entity = esper.create_entity()
    esper.add_component(entity, Position(lat, lon, 0))
    esper.add_component(entity, Hazard(dist, damage_rate=rate))
    esper.add_component(entity, Renderable(image=Path("./icons/hazard.png")))
    return entity
