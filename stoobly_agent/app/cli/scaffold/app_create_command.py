import os
import pdb
import shutil

from .app import App
from .app_command import AppCommand

class AppCreateCommand(AppCommand):

    def __init__(self, app: App, **kwargs):
        super().__init__(app)

    @property
    def app_name(self):
        return self.app.name

    def build(self):
        dest = self.scaffold_namespace_path
        shutil.copytree(self.app_templates_root_dir, dest, dirs_exist_ok=True)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(['**/.env', '**/.config.yml']))

        self.app_config.write()