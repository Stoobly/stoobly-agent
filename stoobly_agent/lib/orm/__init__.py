import os
import pdb

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
            self.initialize_db()

            from stoobly_orator import Model
            self._model = Model
            
    def initialize_db(self):
        config = {
            'default': os.environ.get(ENV) or 'production',
            'test': {
                'driver': 'sqlite',
                'database': DataDir.instance().db_file_path,
            },
            'production': {
                'driver': 'sqlite',
                'database': DataDir.instance().db_file_path,
            }
        }

        from stoobly_orator import DatabaseManager
        db = DatabaseManager(config)

        from stoobly_orator import Model
        Model.set_connection_resolver(db)

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