import logging
from . import config


def setup_logs():
    logging.basicConfig(filename=config.LOG_PATH)
