"""
    Webserver logging configuration file.
    
    It helps for debugging.
    It implements a rotating file handler for the 'webserver.log' file.
    It configures proper UTC timestamp formatting.
"""

import logging
from logging.handlers import RotatingFileHandler
import time

# Configure logger
logger = logging.getLogger('webserver')
logger.setLevel(logging.DEBUG)

def format_time_utc(*_args):

    """
        Get current UTC time
    """

    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

# Set a single formatter with UTC time
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
formatter.formatTime = format_time_utc

# Create rotating file handler for general logs
handler = RotatingFileHandler('webserver.log', maxBytes=10 * 1024 * 1024,
                               backupCount = 5, encoding = 'utf-8')

# Apply formatter to the handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
