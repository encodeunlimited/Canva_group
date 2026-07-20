"""
Logger module for Canva Monitor V2.
Handles daily rotating logs and structured logging for specific events.
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import os

# To ensure config can be imported if app is run as a module or standalone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import LOG_PATH

def setup_logger() -> logging.Logger:
    """
    Configure and return a customized logger instance.
    Logs are written to both standard output and a daily rotating file.
    """
    logger = logging.getLogger("CanvaMonitor")
    logger.setLevel(logging.INFO)

    # Avoid duplicate logs if setup_logger is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (Daily rotation)
    file_handler = TimedRotatingFileHandler(
        filename=LOG_PATH,
        when="midnight",
        interval=1,
        backupCount=30,  # Keep logs for 30 days
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Global logger instance to be used across the application
logger = setup_logger()
