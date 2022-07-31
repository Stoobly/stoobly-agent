import logging
import logging.config
import os
import pdb

from stoobly_agent.config.constants.env_vars import LOG_LEVEL

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DEBUG = 'debug'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'

class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        cls._instance.load()

        return logging

    @classmethod
    def reload(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        cls._instance.load()

    def load(self):
        log_level = os.getenv(LOG_LEVEL) or ''

        if log_level.lower() == DEBUG:
            logging.config.dictConfig({'disable_existing_loggers': True, 'version': 1})
            logging.basicConfig(level=logging.DEBUG)
        elif log_level.lower() == WARNING:
            logging.basicConfig(level=logging.WARNING)
        elif log_level.lower() == ERROR:
            logging.basicConfig(level=logging.ERROR)
        else:
            logging.basicConfig(level=logging.INFO)