import os 
import logging
from logging.handlers import RotatingFileHandler

LOGGING_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}
LOG_LEVEL = LOGGING_LEVELS[os.getenv('LOGGING_LEVEL', 'INFO')]

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
# Create a handler for stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(LOG_LEVEL)
logger.addHandler(stdout_handler)
# Create a handler for the log file
file_handler = RotatingFileHandler('logs/server.log', maxBytes=1024, backupCount=3)
file_handler.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)

