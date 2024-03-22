import pytest

from battleship.component import Hazard, Position

from .damage import get_damage


def test_outside_damage_area() -> None:
    """Further than safe_dist, damage should be zero."""
    hazard = Hazard(safe_dist=10.0, damage_rate=1.0)
    pos_hazard = Position(x=0.0, y=0.0, theta=0.0)
    pos_ship = Position(x=15.0, y=0.0, theta=0.0)

    damage = get_damage(pos_ship, pos_hazard, hazard)
    assert damage == pytest.approx(0.0)


def test_within_damage_area() -> None:
    """Within safe_dist, damage should be non-zero."""
    hazard = Hazard(safe_dist=10.0, damage_rate=1.0)
    pos_hazard = Position(x=0.0, y=0.0, theta=0.0)
    pos_ship = Position(x=5.0, y=0.0, theta=0.0)

    damage = get_damage(pos_ship, pos_hazard, hazard)
    assert damage == pytest.approx(0.5)
