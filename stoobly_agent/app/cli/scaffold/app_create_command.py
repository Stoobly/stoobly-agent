import os
import pathlib
import pdb
import shutil

from .app_command import AppCommand

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

    def build(self):
        dest = os.path.join(self.app_dir_path, self.namespace)
        shutil.copytree(self.__templates_dir, dest, dirs_exist_ok=True)

        self.app_config.write()

    def reset(self):
        dest = os.path.join(self.app_dir_path, self.namespace)

        if os.path.exists(dest) and self.force:
            shutil.rmtree(dest)