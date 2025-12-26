from math import e
import os
import pdb

import shutil
from typing import TypedDict

from stoobly_agent import VERSION
from stoobly_agent.app.cli.scaffold.docker.constants import DOCKER_COMPOSE_WORKFLOW

from .app import App
from .app_command import AppCommand
from .constants import PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT
from .docker.template_files import plugin_docker_cypress, plugin_docker_playwright, plugin_local_cypress, plugin_local_playwright, remove_app_docker_files, remove_service_docker_files
from .templates.constants import CORE_GATEWAY_SERVICE_NAME, CORE_MOCK_UI_SERVICE_NAME, CUSTOM_RUN, MAINTAINED_RUN

class AppCreateOptions(TypedDict):
  docker_socket_path: str
  name: str
  plugin: list
  proxy_port: int
  runtime: list
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

        if kwargs.get('runtime'):
            self.app_config.runtime = kwargs['runtime']

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
    def app_runtime(self):
        return self.app_config.runtime

    @property
    def app_proxy_port(self):
        return self.app_config.proxy_port

    @property
    def app_ui_port(self):
        return self.app_config.ui_port

    @property
    def app_version(self):
        return self.app_config.version

    def build(self):
        self.__migrate()

        dest = self.scaffold_namespace_path
        ignore = []
        warnings = []

        if self.app_config.runtime_local:
            ignore.append(f"{CORE_GATEWAY_SERVICE_NAME}/.*")
            ignore.append(f"{CORE_MOCK_UI_SERVICE_NAME}/.*")

        if self.app_config.runtime_docker:
            ignore.append(f".*/{CUSTOM_RUN}")
            ignore.append(f".*/{MAINTAINED_RUN}")

        # Copy all app templates
        self.app.copy_folders_and_hidden_files(self.app_templates_root_dir, dest, ignore)

        # Remove Docker-specific files if not using Docker
        if not self.app_config.runtime_docker:
            remove_app_docker_files(dest)
            remove_service_docker_files(dest)

        if PLUGIN_CYPRESS in self.app_plugins:
            if not self.__cypress_initialized(self.app):
                warnings.append(f"missing cypress.config.(js|ts), please run `npx cypress open` in {self.app.context_dir_path}")

        if PLUGIN_PLAYWRIGHT in self.app_plugins:
            if not self.__playwright_initialized(self.app):
                warnings.append(f"missing playwright.config.(js|ts), please run `npm init playwright@latest` in {self.app.context_dir_path}")

        if self.app_config.runtime_docker:
            with open(os.path.join(dest, '.gitignore'), 'w') as fp:
                fp.write("\n".join(
                    [os.path.join(CORE_GATEWAY_SERVICE_NAME, '.docker-compose.base.yml'), '**/.env']
                ))

            # Provide plugins
            if PLUGIN_CYPRESS in self.app_plugins:
                plugin_docker_cypress(self.templates_root_dir, PLUGIN_CYPRESS, dest)

            if PLUGIN_PLAYWRIGHT in self.app_plugins:
                plugin_docker_playwright(self.templates_root_dir, PLUGIN_PLAYWRIGHT, dest)
        else:
            if PLUGIN_CYPRESS in self.app_plugins:
                plugin_local_cypress(self.templates_root_dir, PLUGIN_CYPRESS, dest)

            if PLUGIN_PLAYWRIGHT in self.app_plugins:
                plugin_local_playwright(self.templates_root_dir, PLUGIN_PLAYWRIGHT, dest)

            with open(os.path.join(dest, '.gitignore'), 'w') as fp:
                fp.write("\n".join(
                    ['**/.env']
                ))

        self.app_config.write()

        return {
            'warnings': warnings
        }

    def __compare_versions(self, version1, version2):
        """
        Compare two semantic versions.
        
        Args:
            version1: First version string (e.g., '1.10.1')
            version2: Second version string (e.g., '1.9.0')
            
        Returns:
            -1 if version1 < version2
            0 if version1 == version2
            1 if version1 > version2
        """
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for v1_part, v2_part in zip(v1_parts, v2_parts):
                if v1_part < v2_part:
                    return -1
                elif v1_part > v2_part:
                    return 1
            
            return 0
        except (ValueError, AttributeError):
            # If version parsing fails, treat as invalid and return -1 (version1 < version2)
            return -1

    def __migrate(self):
        if not self.app_version or self.__compare_versions(self.app_version, '1.10.0') < 0:
            new_scaffold_namespace_path = self.scaffold_namespace_path
            if not os.path.exists(new_scaffold_namespace_path):
                old_scaffold_namespace_path = os.path.join(self.data_dir_path, 'docker')
                if os.path.exists(old_scaffold_namespace_path):
                    shutil.move(old_scaffold_namespace_path, new_scaffold_namespace_path)
                else:
                    os.makedirs(new_scaffold_namespace_path)

            # For each file in self.scaffold_namespace_path/<SERVICE-NAME>/<WORKFLOW-NAME>/bin 
            # move it to self.scaffold_namespace_path/<SERVICE-NAME>/<WORKFLOW-NAME>
            for service_name in os.listdir(new_scaffold_namespace_path):
                service_path = os.path.join(new_scaffold_namespace_path, service_name)
                if not os.path.isdir(service_path):
                    continue

                for workflow_name in os.listdir(service_path):
                    workflow_path = os.path.join(new_scaffold_namespace_path, service_name, workflow_name)
                    if not os.path.isdir(workflow_path):
                        continue
                    
                    docker_compose_workflow_path = os.path.join(workflow_path, f".docker-compose.{workflow_name}.yml")
                    if os.path.exists(docker_compose_workflow_path):
                        os.rename(docker_compose_workflow_path, os.path.join(workflow_path, DOCKER_COMPOSE_WORKFLOW))

                    bin_path = os.path.join(workflow_path, 'bin')
                    if not os.path.isdir(bin_path):
                        continue

                    for file in os.listdir(bin_path):
                        shutil.move(os.path.join(bin_path, file), os.path.join(workflow_path, file))

                    # Remove the bin folder
                    shutil.rmtree(bin_path)

            self.app_config.version = VERSION
            self.app_config.write()

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