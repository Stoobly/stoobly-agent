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

        self.__copy_folders_and_hidden_files(self.app_templates_root_dir, dest)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(['**/.env', '**/.config.yml']))

        self.app_config.write()

    def __copy_folders_and_hidden_files(self, src, dst):
        os.makedirs(dst, exist_ok=True)

        # Walk through the source directory
        for root, dirs, files in os.walk(src):
            # Copy hidden files only
            for file_name in files:
                src_file_path = os.path.join(root, file_name)
                dst_file_path = os.path.join(dst, os.path.relpath(root, src), file_name)

                if not file_name.startswith('.'):
                    if os.path.exists(dst_file_path):
                        continue

                os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)  # Create directories in destination
                shutil.copy2(src_file_path, dst_file_path)