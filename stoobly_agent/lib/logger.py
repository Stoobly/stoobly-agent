import logging
import os

from .env_vars import LOG_LEVEL

class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            log_level = os.getenv(LOG_LEVEL)

            if log_level == 'debug':
                logging.basicConfig(level=logging.DEBUG)
            elif log_level == 'warning':
                logging.basicConfig(level=logging.WARNING)
            elif log_level == 'error':
                logging.basicConfig(level=logging.ERROR)
            else:
                logging.basicConfig(level=logging.INFO)

        return logging

