import os
import shutil
import yaml

from mergedeep import merge

from ..constants import PLUGINS_FOLDER, WORKFLOW_TEST_TYPE
from ..templates.constants import CORE_ENTRYPOINT_SERVICE_NAME
from .constants import (
  DOCKER_COMPOSE_BASE_TEMPLATE,
  DOCKER_COMPOSE_CUSTOM,
  DOCKER_COMPOSE_WORKFLOW,
  DOCKER_MAKEFILE,
  DOCKER_MAKEFILE_DOT,
  DOCKERFILE_CONTEXT,
  DOCKER_COMPOSE_BASE,
  DOCKER_COMPOSE_NETWORKS,
  PLUGIN_CONTAINER_SERVICE_TEMPLATE,
  PLUGIN_DOCKER_ENTRYPOINT,
  PLUGIN_DOCKERFILE_TEMPLATE,
)

DOCKER_APP_TEMPLATE_FILES = [
  DOCKER_MAKEFILE,
  DOCKER_MAKEFILE_DOT,
  DOCKERFILE_CONTEXT,
  DOCKER_COMPOSE_BASE,
  DOCKER_COMPOSE_NETWORKS,
]

def __merge_compose_plugin(dest_path: str, template_path: str, plugin: str):
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

def remove_app_docker_files(dest_path: str):
  for file_name in DOCKER_APP_TEMPLATE_FILES:
      file_path = os.path.join(dest_path, file_name)
      if os.path.exists(file_path):
          os.remove(file_path)

def remove_service_docker_files(service_path: str):
  compose_files = [DOCKER_COMPOSE_BASE, DOCKER_COMPOSE_CUSTOM, DOCKER_COMPOSE_BASE_TEMPLATE]

  # For each file in dest_path recursively, check whether it is DOCKER_COMPOSE_BASE or DOCKER_COMPOSE_BASE_TEMPLATE, if so remove it
  for root, _, files in os.walk(service_path):
      for file in files:
          if file in compose_files or file == DOCKER_COMPOSE_WORKFLOW:
              os.remove(os.path.join(root, file))

def plugin_docker_cypress(templates_root_dir: str, plugin: str, dest: str):
  dockerfile_name = PLUGIN_DOCKERFILE_TEMPLATE.format(plugin=plugin)
  dockerfile_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, dockerfile_name)

  # Copy Dockerfile to workflow
  dockerfile_src_path = os.path.join(templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, dockerfile_name)
  shutil.copyfile(dockerfile_src_path, dockerfile_dest_path)

  # Merge template into dest compose yml
  compose_dest_path = os.path.join(
      dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW
  )
  template_path = os.path.join(
      templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW
  )
  __merge_compose_plugin(compose_dest_path, template_path, plugin)

def plugin_docker_playwright(templates_root_dir: str, plugin: str, dest: str):
  dockerfile_name = PLUGIN_DOCKERFILE_TEMPLATE.format(plugin=plugin)
  dockerfile_src_path = os.path.join(templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, dockerfile_name)
  dockerfile_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, dockerfile_name)
  shutil.copyfile(dockerfile_src_path, dockerfile_dest_path)

  entrypoint_src_path = os.path.join(templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, PLUGIN_DOCKER_ENTRYPOINT)
  entrypoint_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, PLUGIN_DOCKER_ENTRYPOINT)
  shutil.copyfile(entrypoint_src_path, entrypoint_dest_path)

  # Merge template into dest compose yml
  compose_dest_path = os.path.join(
      dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW
  )
  template_path = os.path.join(
      templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, DOCKER_COMPOSE_WORKFLOW
  )
  __merge_compose_plugin(compose_dest_path, template_path, plugin)

def plugin_local_cypress(templates_root_dir: str, plugin: str, dest: str):
  # Copy run script
  run_script_src_path = os.path.join(templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, '.run')
  run_script_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, '.run')
  # Use shutil.copy instead of shutil.copyfile to preserve permissions
  shutil.copy(run_script_src_path, run_script_dest_path)

def plugin_local_playwright(templates_root_dir: str, plugin: str, dest: str):
  # Copy run script
  run_script_src_path = os.path.join(templates_root_dir, PLUGINS_FOLDER, plugin, WORKFLOW_TEST_TYPE, '.run')
  run_script_dest_path = os.path.join(dest, CORE_ENTRYPOINT_SERVICE_NAME, WORKFLOW_TEST_TYPE, '.run')
  shutil.copy(run_script_src_path, run_script_dest_path)