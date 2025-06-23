import os
import pdb
import shutil
import yaml

from typing import TypedDict

from .app import App
from .app_command import AppCommand
from .constants import PLUGIN_CYPRESS, WORKFLOW_TEST_TYPE
from .docker.constants import DOCKER_COMPOSE_CUSTOM, PLUGIN_CONTAINER_SERVICE, PLUGIN_DOCKERFILE
from .templates.constants import CORE_ENTRYPOINT_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME

class AppCreateOptions(TypedDict):
  name: str
  network: str

class AppCreateCommand(AppCommand):

    def __init__(self, app: App, **kwargs: AppCreateOptions):
        super().__init__(app)

        if kwargs.get('app_name'):
            self.app_config.name = kwargs['app_name']

        if kwargs.get('network'):
            self.app_config.network = kwargs['network']

        if kwargs.get('plugin'):
            self.app_config.plugins = kwargs['plugin']

    @property
    def app_name(self):
        return self.app_config.name

    @property
    def app_network(self):
        return self.app_config.network

    @property
    def app_plugins(self):
        return self.app_config.plugins

    def build(self):
        dest = self.scaffold_namespace_path

        self.app.copy_folders_and_hidden_files(self.app_templates_root_dir, dest)

        if PLUGIN_CYPRESS in self.app_plugins:
            self.__plugin_with_docker(dest, PLUGIN_CYPRESS)

        with open(os.path.join(dest, '.gitignore'), 'w') as fp:
            fp.write("\n".join(
                [os.path.join(CORE_GATEWAY_SERVICE_NAME, '.docker-compose.base.yml'), '**/.env']
            ))

        self.app_config.write()

    def __plugin_with_docker(self, dest: str, plugin: str):
        dockerfile_name = PLUGIN_DOCKERFILE.format(plugin=plugin)
        dockerfile_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, dockerfile_name)

        if not os.path.exists(dockerfile_dest_path):
            dockerfile_src_path = os.path.join(self.templates_root_dir, 'plugins', plugin, WORKFLOW_TEST_TYPE, dockerfile_name)
            shutil.copyfile(dockerfile_src_path, dockerfile_dest_path)
        
        # Merge template into dest 
        compose_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_CUSTOM)
        self.__plugin_compose(compose_dest_path, PLUGIN_CYPRESS)

    def __plugin_compose(self, dest_path: str, plugin: str):
        template_path = os.path.join(self.templates_root_dir, 'plugins', plugin, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_CUSTOM)

        if not os.path.exists(dest_path):
            open(dest_path, 'a').close()

        def load_yaml(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}

        data1 = load_yaml(dest_path)
        data2 = load_yaml(template_path)

        services = data1.get('services') or {}
        if services.get(PLUGIN_CONTAINER_SERVICE.format(plugin=plugin, service=CORE_ENTRYPOINT_SERVICE_NAME)):
            return

        with open(dest_path, 'w') as out:
            merged = { **data1, **data2 } 
            yaml.dump(merged, out, default_flow_style=False)