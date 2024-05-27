import os
import pathlib
import pdb
import shutil

from .app_command import AppCommand
from .constants import ENV_FILE
from .config import Config

class AppCreateCommand(AppCommand):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__app_name = kwargs['app_name']
        self.__force = not not kwargs.get('force')
        self.__templates_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'templates', 'app')

    @property
    def app_name(self):
        return self.__app_name

    @property
    def force(self):
        return self.__force

    def build_with_docker(self):
        self.as_docker()
        dest = os.path.join(self.app_dir_path, self.namespace)

        if os.path.exists(dest) and self.force:
            shutil.rmtree(dest)

        shutil.copytree(self.__templates_dir, dest, dirs_exist_ok=True)

        self.write_config()

    def write_config(self):
        env_vars = {
            'NETWORK': self.app_name
        }

        config_path = self.app_config_path
        Config(config_path).write(env_vars)       