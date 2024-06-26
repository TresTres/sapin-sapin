import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Config

LOGGING_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

logger = logging.getLogger(__name__)


def configure_logging(config: Config) -> None:
    """
    Configure the logging level and handlers.
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_level = LOGGING_LEVELS[config.get("LOG_LEVEL", "INFO")]
    logger.setLevel(log_level)
    # Create a handler for stdout
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    # Create a handler for the log file
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler("logs/server.log", maxBytes=1024, backupCount=3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
