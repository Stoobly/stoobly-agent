import os
import pdb
import tempfile

class DataDir:
    DATA_DIR_NAME = '.stoobly'
    DB_FILE_NAME = 'stoobly_agent.sqlite3'

    _instance = None

    def __init__(self):
        if DataDir._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.__data_dir_path = os.path.join(os.path.expanduser('~'), self.DATA_DIR_NAME)

            if not os.path.exists(self.__data_dir_path):
                os.mkdir(self.__data_dir_path)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def path(self):
        return self.__data_dir_path

    @property
    def tmp_dir_path(self):
        tmp_dir_path = os.path.join(self.path, 'tmp')

        if not os.path.exists(tmp_dir_path):
            os.mkdir(tmp_dir_path)

        return tmp_dir_path

    @property
    def db_dir_path(self):
        db_dir_path = os.path.join(self.path, 'db')

        if not os.path.exists(db_dir_path):
            os.mkdir(db_dir_path)

        return db_dir_path

    @property
    def tmp_db_file_path(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        return tmp.name

    @property
    def db_file_path(self):
        return os.path.join(self.db_dir_path, self.DB_FILE_NAME)

    @property
    def settings_file_path(self):
        return os.path.join(self.path, 'settings.yml')
