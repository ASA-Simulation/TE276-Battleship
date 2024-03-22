"""Path planning module: responsible for computing the action/heading to take."""

# Uncomment line below to use the naive solution:
# approach the target ignoring all hazards.
# from .naive import naive as plan_action

# Uncomment line below to use another solution:
# compute the heading using potential fields attracting
# to target and repulsing from hazards.
from .potential_field import potential_field as plan_action  # noqa: F401
