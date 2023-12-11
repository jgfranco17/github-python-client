"""Declares this directory as a Python module."""
import logging

from .client import GithubClient  # noqa E501

LOGLEVEL = "DEBUG"


def __set_logging_level(level: str) -> None:
    """Set the logging level.

    Args:
        level (str): Level of logging for package
    """
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logging.basicConfig(
        level=levels.get(level, logging.INFO),
        format="[%(asctime)s | %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d | %H:%M:%S",
    )
    logging.info(f"Set logging level to {level}")


__set_logging_level(LOGLEVEL)
