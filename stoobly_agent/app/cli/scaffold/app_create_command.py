import os
import pdb

from typing import TypedDict

from .app import App
from .app_command import AppCommand
from .constants import PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT, RUN_ON_DOCKER
from .docker.template_files import plugin_cypress, plugin_playwright, remove_app_docker_files, remove_service_docker_files
from .templates.constants import CORE_GATEWAY_SERVICE_NAME

class AppCreateOptions(TypedDict):
  docker_socket_path: str
  name: str
  plugin: list
  proxy_port: int
  run_on: list
  ui_port: int

class AppCreateCommand(AppCommand):

    def __init__(self, app: App, **kwargs: AppCreateOptions):
        super().__init__(app)

        if kwargs.get('app_name'):
            self.app_config.name = kwargs['app_name']

        if kwargs.get('docker_socket_path'):
            self.app_config.docker_socket_path = kwargs['docker_socket_path']

        if kwargs.get('plugin'):
            self.app_config.plugins = kwargs['plugin']

        if kwargs.get('proxy_port'):
            self.app_config.proxy_port = kwargs['proxy_port']

        if kwargs.get('run_on'):
            self.app_config.run_on = kwargs['run_on']

        if kwargs.get('ui_port'):
            self.app_config.ui_port = kwargs['ui_port']

    @property
    def docker_socket_path(self):
        return self.app_config.docker_socket_path

    @property
    def app_name(self):
        return self.app_config.name

    @property
    def app_plugins(self):
        return self.app_config.plugins

    @property
    def app_run_on(self):
        return self.app_config.run_on

    def app_proxy_port(self):
        return self.app_config.proxy_port

    def app_ui_port(self):
        return self.app_config.ui_port

    def build(self):
        dest = self.scaffold_namespace_path
        warnings = []

        # Copy all app templates
        self.app.copy_folders_and_hidden_files(self.app_templates_root_dir, dest)

        # Remove Docker-specific files if not using Docker
        if RUN_ON_DOCKER not in self.app_run_on:
            remove_app_docker_files(dest)
            remove_service_docker_files(dest)

        if PLUGIN_CYPRESS in self.app_plugins:
            if not self.__cypress_initialized(self.app):
                warnings.append(f"missing cypress.config.(js|ts), please run `npx cypress open` in {self.app.context_dir_path}")

        if PLUGIN_PLAYWRIGHT in self.app_plugins:
            if not self.__playwright_initialized(self.app):
                warnings.append(f"missing playwright.config.(js|ts), please run `npm init playwright@latest` in {self.app.context_dir_path}")

        if RUN_ON_DOCKER in self.app_run_on:
            with open(os.path.join(dest, '.gitignore'), 'w') as fp:
                fp.write("\n".join(
                    [os.path.join(CORE_GATEWAY_SERVICE_NAME, '.docker-compose.base.yml'), '**/.env']
                ))

            # Provide plugins
            if PLUGIN_CYPRESS in self.app_plugins:
                plugin_cypress(self.templates_root_dir, PLUGIN_CYPRESS, dest)

            if PLUGIN_PLAYWRIGHT in self.app_plugins:
                plugin_playwright(self.templates_root_dir, PLUGIN_PLAYWRIGHT, dest)
        else:
            with open(os.path.join(dest, '.gitignore'), 'w') as fp:
                fp.write("\n".join(
                    ['**/.env']
                ))

        self.app_config.write()

        return {
            'warnings': warnings
        }

    def __cypress_initialized(self, app: App):
        if os.path.exists(os.path.join(app.context_dir_path, 'cypress.config.js')):
            return True
            
        if os.path.exists(os.path.join(app.context_dir_path, 'cypress.config.ts')):
            return True

        return False

    def __playwright_initialized(self, app: App):
        if os.path.exists(os.path.join(app.context_dir_path, 'playwright.config.js')):
            return True
            
        if os.path.exists(os.path.join(app.context_dir_path, 'playwright.config.ts')):
            return True

        return False