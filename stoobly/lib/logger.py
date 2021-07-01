import logging
import os

class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            env = os.getenv('PROXY_ENV')

            if env == 'production':
                logging.basicConfig(level=logging.WARNING)
            elif env == 'staging':
                logging.basicConfig(level=logging.INFO)
            else:
                logging.basicConfig(level=logging.DEBUG)

        return logging

