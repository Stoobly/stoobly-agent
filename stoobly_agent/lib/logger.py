import logging
import logging.config
import os
import pdb
import sys

from typing import Literal

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
LogLevel = Literal[DEBUG, ERROR, INFO, WARNING]

class Logger:
    _instance = None
    _instances = {}

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, name = None):
        if cls._instance is None:
            logging.getLogger("mitmproxy").setLevel(logging.ERROR)
            cls._instance = cls.__new__(cls)
            cls._instance.load()

        if not name:
            name = 'root'

        logger = logging.getLogger(name)

        if name not in cls._instances:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(f"[%(levelname)s] {name} %(message)s"))
            logger.addHandler(handler)
            logger.propagate = False
            cls._instances[name] = logger

        return logger

    @classmethod
    def reload(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        cls._instance.load()

    def load(self):
        log_level = (os.getenv(LOG_LEVEL) or INFO).lower()
        levels = {
            DEBUG: logging.DEBUG,
            INFO: logging.INFO,
            WARNING: logging.WARNING,
            ERROR: logging.ERROR,
        }
        level = levels.get(log_level, logging.INFO)

        # basicConfig is a no-op once root has handlers; always setLevel so reload works
        # after CLI commands mutate STOOBLY_AGENT_LOG_LEVEL mid-process.
        if log_level == DEBUG:
            logging.config.dictConfig({'disable_existing_loggers': True, 'version': 1})
        logging.basicConfig(level=level, stream=sys.stderr)
        logging.getLogger().setLevel(level)

        for logger in self._instances.values():
            # dictConfig(disable_existing_loggers=True) marks prior loggers disabled;
            # re-enable so reload to debug does not silence cached named loggers.
            logger.disabled = False
            logger.setLevel(level)