import logging
import sys
<<<<<<< HEAD

from whykay.config import LOG_LEVEL

=======
from whykay.config import *
>>>>>>> a49278411eaa38fce3d57fb54577e9b3d996108e

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
