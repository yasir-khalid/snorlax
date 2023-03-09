import logging
import sys
from whykay.config import *

def init_logger(name):
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(console_formatter)
    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.setLevel(LOG_LEVEL)
    return logger
