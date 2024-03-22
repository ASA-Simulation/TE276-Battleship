import pygame

from battleship.config import logger
from battleship.factory import new_hazard, new_ship
from battleship.processor import (
    DamageProcessor,
    MoveProcessor,
    ReasonProcessor,
    RenderProcessor,
)
from battleship.resource import TimeResource
from battleship.utils import has_alive

_logger = logger.getChild(__name__)


def initialization(dt: float) -> None:
    # Initialize time resource with desired simulation step
    TimeResource().set_dt(dt)
    # Initialize the ship
    new_ship(
        x=1_000.0,
        y=3_000.0,
        nav=[
            (3_000.0, 3_000.0),
            (4_000.0, 4_000.0),
            (5_000.0, 3_000.0),
            (4_000.0, 2_000.0),
            (3_000.0, 3_000.0),
            # (1_000.0, 3_000.0),
        ],
    )
    # Initialize all hazards
    new_hazard(3_500.0, 2_500.0, 200, 0.21)
    new_hazard(4_500.0, 2_500.0, 200, 0.21)
    new_hazard(4_000.0, 3_000.0, 200, 0.21)
    new_hazard(3_500.0, 3_500.0, 200, 0.21)
    new_hazard(4_500.0, 3_500.0, 200, 0.21)


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    window = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Battleship Simulator")
    clock = pygame.time.Clock()
    running = True

    # simulation setup (simulation rate = 100Hz)
    initialization(dt=(1.0 / 100.0))

    # creating processors (systems in the ECS terminology)
    render = RenderProcessor(window, width=720, height=720, fps=24)
    reasoner = ReasonProcessor()
    mover = MoveProcessor(velocity=10.0, turn_rate=10.0)
    damager = DamageProcessor()

    #
    # main execution loop
    #

    step = 0
    timer = TimeResource()

    while True:
        # poll for events (only QUIT treated)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        # fill the screen with a color to wipe away anything from last frame
        window.fill("purple")

        # reasoning rate is slower (10Hz)
        if step % 10 == 0:
            if not reasoner.process():
                break

        # these processors run at full rate
        mover.process()
        damager.process()

        # render is internally limited to screen FPS
        render.process()

        # early termination checks
        if not has_alive():
            _logger.warn("Early stopping execution due to: there is no entity alive")
            break

        step += 1
        timer.add_time()

    # pygame cleanup
    pygame.quit()
