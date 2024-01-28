import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler for stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

# Create a handler for the log file
file_handler = RotatingFileHandler('logs/server.log', maxBytes=1024, backupCount=3)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

