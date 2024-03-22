"""All processors that bring dynamism to the simulation."""

from abc import ABC, abstractmethod


class AbstractProcessor(ABC):
    @abstractmethod
    def process(self) -> bool:
        """
        This method, to be implemented by all processors, performs the computation
        and returns whether simulation should continue.
        """
        raise NotImplementedError("AbstractProcessor.process not implemented")


#
# Re-exported processors
#

from .damage import DamageProcessor  # noqa: F401
from .move import MoveProcessor  # noqa: F401
from .reason import ReasonProcessor  # noqa: F401
from .render import RenderProcessor  # noqa: F401
