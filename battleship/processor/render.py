from math import degrees, floor
from typing import Tuple

import esper
import pygame
from pygame import Color, Rect
from pygame.font import Font
from pygame.surface import Surface
from pygame.time import Clock, get_ticks
from pygame.transform import rotate

from battleship.component import Position, Renderable
from battleship.resource import TimeResource

from . import AbstractProcessor


def reframe(
    position: Position, size: float, width: float, height: float
) -> Tuple[float, float]:
    return (
        (position.x / size) * width,
        (position.y / size) * height,
    )


class RenderProcessor(AbstractProcessor):
    """
    Processor that performs all rendering.
    """

    def __init__(
        self,
        window: Surface,
        width: float,
        height: float,
        clear_color=(255, 255, 255),
        fps=24,
    ):
        super().__init__()
        # display management
        self.window = window
        self.width = width
        self.height = height
        self.clear_color = clear_color
        self.fps = fps
        # timer management
        self.font = Font(None, 21)
        self.clock = Clock()
        self.speedup = 0.0
        self.alpha = 0.1
        # speedup calculation
        self.last_real_time = get_ticks()
        self.last_simu_time = TimeResource().get_time()

    def process(self) -> bool:
        real_time = get_ticks()
        simu_time = TimeResource().get_time()

        # should we re-render screen (stick to fps)
        if (real_time - self.last_real_time) < (1_000 / self.fps):
            return

        # clear the window:
        self.window.fill(self.clear_color)

        for _, (position, renderable) in esper.get_components(Position, Renderable):
            #
            # Iterate over all renderable components (Position + Renderable)
            #
            self._render_component(position, renderable)

        self._render_timer(real_time, simu_time)

        # flip the framebuffers
        pygame.display.flip()

        # update last values for the next call
        self.last_real_time = real_time
        self.last_simu_time = simu_time

    def _render_component(self, position: Position, component: Renderable) -> None:
        # render the given component
        self.window.blit(
            rotate(component.image, -degrees(position.theta)),
            reframe(
                position=position,
                size=6_000.0,
                width=self.width,
                height=self.height,
            ),
        )

    def _render_timer(self, real_time: int, simu_time: float) -> None:
        # convert all times to milliseconds
        delta_real_time = real_time - self.last_real_time
        delta_simu_time = floor(1_000.0 * (simu_time - self.last_simu_time))

        # smooth speedup estimation
        self.speedup = (1 - self.alpha) * self.speedup + self.alpha * (
            delta_simu_time / delta_real_time
        )

        # build message and render it
        msg = f"Simulation Rate = {TimeResource().get_rate()} | Speedup = {self.speedup:.1f}"
        self.window.blit(self.font.render(msg, True, Color("red")), Rect(0, 0, 25, 25))
