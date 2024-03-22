import logging
from logging import Logger

#
# Here we set the logging level
# levels: FATAL > ERROR > WARN > INFO > DEBUG > NOTSET
#
logging.basicConfig(
    filename=None,
    level=logging.INFO,
    format="%(asctime)s <%(levelname)s> [%(name)s] %(message)s",
)

# root logger
logger: Logger = logging.getLogger(None)
