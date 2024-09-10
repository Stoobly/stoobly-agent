import os
import pdb
import shutil

from .app_command import AppCommand

class AppCreateCommand(AppCommand):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__app_name = kwargs.get('app_name') or os.path.basename(self.app_dir_path)
        self.__force = not not kwargs.get('force')

    @property
    def app_name(self):
        return self.__app_name

    @property
    def force(self):
        return self.__force

    def build(self):
        dest = os.path.join(self.app_dir_path, self.namespace)
        shutil.copytree(self.app_templates_root_dir, dest, dirs_exist_ok=True)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(['**/.env', '**/.yml']))

        self.app_config.write()

    def reset(self):
        dest = os.path.join(self.app_dir_path, self.namespace)

        if os.path.exists(dest) and self.force:
            shutil.rmtree(dest)