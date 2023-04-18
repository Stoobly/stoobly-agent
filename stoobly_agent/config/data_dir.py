import os
import pdb
import shutil

from stoobly_agent.config.constants.env_vars import ENV

class DataDir:
    DATA_DIR_NAME = '.stoobly'
    DB_FILE_NAME = 'stoobly_agent.sqlite3'
    DB_VERSION_NAME = 'VERSION'

    _instance = None

    def __init__(self):
        if DataDir._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.__data_dir_path = os.path.join(os.getcwd(), self.DATA_DIR_NAME)

            # If the current working directory does not contain a .stoobly folder, default to home directory
            if not os.path.exists(self.__data_dir_path):
                self.__data_dir_path = os.path.join(os.path.expanduser('~'), self.DATA_DIR_NAME)

            if not os.path.exists(self.__data_dir_path):
                os.makedirs(self.__data_dir_path, exist_ok=True)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def path(self):
        if os.environ.get(ENV) == 'test':
            test_path = os.path.join(self.__data_dir_path, 'tmp', self.DATA_DIR_NAME)
            
            if not os.path.exists(test_path):
                os.makedirs(test_path, exist_ok=True)
            return test_path

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
    def db_file_path(self):
        return os.path.join(self.db_dir_path, self.DB_FILE_NAME)

    @property
    def db_version_path(self):
        return os.path.join(self.db_dir_path, self.DB_VERSION_NAME)

    @property
    def settings_file_path(self):
        return os.path.join(self.path, 'settings.yml')

    def remove(self):
        if os.path.exists(self.path):
           shutil.rmtree(self.path) 

    def create(self, directoy_path = None):
        if not directoy_path:
            directoy_path = os.getcwd()

        self.__data_dir_path = os.path.join(directoy_path, self.DATA_DIR_NAME)

        if not os.path.exists(self.__data_dir_path):
            os.mkdir(self.__data_dir_path)