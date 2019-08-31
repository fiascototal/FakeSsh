import logging
from fake_ssh import config


def setup_logs():
    logging.basicConfig(filename=config.LOG_PATH)
