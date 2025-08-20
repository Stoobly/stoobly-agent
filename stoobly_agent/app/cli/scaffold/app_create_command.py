import os
import pdb
import shutil
import yaml

from mergedeep import merge
from typing import TypedDict

from .app import App
from .app_command import AppCommand
from .constants import PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT, PLUGINS_FOLDER, WORKFLOW_TEST_TYPE
from .docker.constants import DOCKER_COMPOSE_WORKFLOW_TEMPLATE, PLUGIN_CONTAINER_SERVICE_TEMPLATE, PLUGIN_DOCKER_ENTRYPOINT, PLUGIN_DOCKERFILE_TEMPLATE
from .templates.constants import CORE_ENTRYPOINT_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME

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

        if kwargs.get('plugin'):
            self.app_config.plugins = kwargs['plugin']

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

    def app_ui_port(self):
        return self.app_config.ui_port

    def build(self):
        dest = self.scaffold_namespace_path

        self.app.copy_folders_and_hidden_files(self.app_templates_root_dir, dest)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(
                [os.path.join(CORE_GATEWAY_SERVICE_NAME, '.docker-compose.base.yml'), '**/.env']
            ))

        self.app_config.write()

        # Provide plugins
        warnings = []
        if PLUGIN_CYPRESS in self.app_plugins:
            self.__plugin_cypress(dest, PLUGIN_CYPRESS)

            if not self.__cypress_initialized(self.app):
                warnings.append(f"missing cypress.config.(js|ts), please run `npx cypress open` in {self.app.context_dir_path}")


        if PLUGIN_PLAYWRIGHT in self.app_plugins:
            self.__plugin_playwright(dest, PLUGIN_PLAYWRIGHT)

            if not self.__playwright_initialized(self.app):
                warnings.append(f"missing playwright.config.(js|ts), please run `npm init playwright@latest` in {self.app.context_dir_path}")

        return {
            'warnings': warnings
        }

    def __cypress_initialized(self, app: App):
        if os.path.exists(os.path.join(app.context_dir_path, 'cypress.config.js')):
            return True
            
        if os.path.exists(os.path.join(app.context_dir_path, 'cypress.config.ts')):
            return True

        return False

    def __merge_compose_plugin(self, dest_path: str, template_path: str, plugin: str):
        if not os.path.exists(dest_path):
            open(dest_path, 'a').close()

        def load_yaml(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}

        data1 = load_yaml(dest_path)
        data2 = load_yaml(template_path)

        services = data1.get('services') or {}
        if services.get(PLUGIN_CONTAINER_SERVICE_TEMPLATE.format(plugin=plugin, service=CORE_ENTRYPOINT_SERVICE_NAME)):
            return

        with open(dest_path, 'w') as out:
            merged = merge(data1, data2)
            yaml.dump(merged, out, default_flow_style=False)

    def __playwright_initialized(self, app: App):
        if os.path.exists(os.path.join(app.context_dir_path, 'playwright.config.js')):
            return True
            
        if os.path.exists(os.path.join(app.context_dir_path, 'playwright.config.ts')):
            return True

        return False

    def __plugin_cypress(self, dest: str, plugin: str):
        dockerfile_name = PLUGIN_DOCKERFILE_TEMPLATE.format(plugin=plugin)
        dockerfile_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, dockerfile_name)

        # Copy Dockerfile to workflow
        dockerfile_src_path = os.path.join(self.templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, dockerfile_name)
        shutil.copyfile(dockerfile_src_path, dockerfile_dest_path)

        # Merge template into dest compose yml
        compose_dest_path = os.path.join(
            dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW_TEMPLATE.format(workflow=WORKFLOW_TEST_TYPE)
        )
        template_path = os.path.join(
            self.templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW_TEMPLATE.format(workflow=WORKFLOW_TEST_TYPE)
        )
        self.__merge_compose_plugin(compose_dest_path, template_path, plugin)

    def __plugin_playwright(self, dest: str, plugin: str):
        # Copy Dockerfile to workflow
        dockerfile_name = PLUGIN_DOCKERFILE_TEMPLATE.format(plugin=plugin)
        dockerfile_src_path = os.path.join(self.templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, dockerfile_name)
        dockerfile_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, dockerfile_name)
        shutil.copyfile(dockerfile_src_path, dockerfile_dest_path)

        entrypoint_src_path = os.path.join(self.templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, PLUGIN_DOCKER_ENTRYPOINT)
        entrypoint_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, PLUGIN_DOCKER_ENTRYPOINT)
        shutil.copyfile(entrypoint_src_path, entrypoint_dest_path)

        # Merge template into dest compose yml
        compose_dest_path = os.path.join(
            dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW_TEMPLATE.format(workflow=WORKFLOW_TEST_TYPE)
        )
        template_path = os.path.join(
            self.templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW_TEMPLATE.format(workflow=WORKFLOW_TEST_TYPE)
        )
        self.__merge_compose_plugin(compose_dest_path, template_path, plugin)