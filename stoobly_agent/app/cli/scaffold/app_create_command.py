import os
import pdb

from typing import TypedDict

from .app import App
from .app_command import AppCommand

class AppCreateOptions(TypedDict):
  docker_socket_path: str
  name: str
  ui_port: int

class AppCreateCommand(AppCommand):

    def __init__(self, app: App, **kwargs: AppCreateOptions):
        super().__init__(app)

        if kwargs.get('app_name'):
            self.app_config.name = kwargs['app_name']

        if kwargs.get('docker_socket_path'):
            self.app_config.docker_socket_path = kwargs['docker_socket_path']

        if kwargs.get('ui_port'):
            self.app_config.ui_port = kwargs['ui_port']

    @property
    def docker_socket_path(self):
        return self.app_config.docker_socket_path

    @property
    def app_name(self):
        return self.app_config.name

    @property
    def app_ui_port(self):
        return self.app_config.ui_port

    def build(self):
        dest = self.scaffold_namespace_path

        self.app.copy_folders_and_hidden_files(self.app_templates_root_dir, dest)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(['gateway/.docker-compose.base.yml', '**/.env']))

        self.app_config.write()