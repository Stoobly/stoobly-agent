import os
import pdb

class SourceDir:
    _instance = None

    def __init__(self):
        if SourceDir._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.__src_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def path(self):
        return self.__src_dir_path

    @property
    def config_dir_path(self):
        return os.path.join(self.path, 'config')

    @property
    def db_dir_path(self):
        return os.path.join(self.path, 'db')

    @property
    def db_migrations_dir_path(self):
        return os.path.join(self.db_dir_path, 'migrations')

    @property
    def settings_file_path(self):
        return os.path.join(self.config_dir_path, 'settings.yml')

    @property
    def settings_template_file_path(self):
        return os.path.join(self.config_dir_path, 'settings.yml.sample')

    @property
    def schema_file_path(self):
        return os.path.join(self.config_dir_path, 'schema.yml')