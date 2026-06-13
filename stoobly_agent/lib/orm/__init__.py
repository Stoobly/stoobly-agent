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
            self._data_dir_path = None
            self.initialize_db()

            from stoobly_orator import Model
            self._model = Model

    def initialize_db(self, data_dir_path: str = None):
        if self._data_dir_path == data_dir_path and self._db is not None:
            return

        self._data_dir_path = data_dir_path

        config = {
            'default': os.environ.get(ENV) or 'production',
            'test': {
                'driver': 'sqlite',
                'database': DataDir.instance(data_dir_path).db_file_path,
            },
            'production': {
                'driver': 'sqlite',
                'database': DataDir.instance(data_dir_path).db_file_path,
            }
        }

        from stoobly_orator import DatabaseManager
        db = DatabaseManager(config)

        from stoobly_orator import Model
        Model.set_connection_resolver(db)

        self._db = db

    @classmethod
    def configure(cls, data_dir_path: str = None):
        cls.instance().initialize_db(data_dir_path)

    @classmethod
    def handle_chdir(cls):
        DataDir.handle_chdir()
        instance = cls.instance()
        if instance._data_dir_path is None:
            instance.initialize_db(None)

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
