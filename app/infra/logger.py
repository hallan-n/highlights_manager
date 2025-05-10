import sys

from loguru import logger

logger.remove()

logger.add(
    sys.stderr,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<8} | "
        "{file}:{line} | "
        "{message:<50}"
    ),
    level="DEBUG",
)
