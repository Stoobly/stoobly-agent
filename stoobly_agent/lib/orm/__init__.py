import os
import pdb

from orator import DatabaseManager, Model

from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.config.data_dir import DataDir

class ORM():
    _instance = None
    _model = None
    _db = None

    def __init__(self):
        if ORM._instance:
            raise RuntimeError('Call instance() instead')
        else:
            config = {
                'default': os.environ.get(ENV) or 'production',
                'test': {
                    'driver': 'sqlite',
                    'database': DataDir.instance().tmp_db_file_path,
                },
                'production': {
                    'driver': 'sqlite',
                    'database': DataDir.instance().db_file_path,
                }
            }

            db = DatabaseManager(config)
            Model.set_connection_resolver(db)

            self._model = Model
            self._db = db

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def base(self):
        return self._model

    @property
    def db(self):
        return self._db