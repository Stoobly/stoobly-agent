import os
import pdb
import shutil
import yaml

from typing import List

from stoobly_agent.config.data_dir import DATA_DIR_NAME, TMP_DIR_NAME
from stoobly_agent.app.cli.scaffold.constants import APP_DIR
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.docker.constants import APP_INGRESS_NETWORK_NAME, APP_EGRESS_NETWORK_NAME, DOCKER_COMPOSE_BASE, DOCKER_COMPOSE_BASE_TEMPLATE, GATEWAY_NGINX_TEMPLATE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME
from stoobly_agent.app.cli.scaffold.templates import run_template_path

def configure_gateway(service_paths: List[str], no_publish = False):
  if len(service_paths) == 0:
    return

  hostnames, ports = __find_hosts(service_paths)

  service_dir_path = os.path.dirname(service_paths[0])
  gateway_service_path = os.path.join(service_dir_path, CORE_GATEWAY_SERVICE_NAME)
  docker_compose_src_path = os.path.join(gateway_service_path, DOCKER_COMPOSE_BASE_TEMPLATE)
  docker_compose_dest_path = os.path.join(gateway_service_path, DOCKER_COMPOSE_BASE)

  compose = {}
  with open(docker_compose_src_path, 'r') as fp:
    compose = yaml.safe_load(fp)
    services = compose.get('services')

    if not services:
      return
    
    gateway_base = services.get('gateway_base')

    if gateway_base:
      if not no_publish:
        gateway_base['ports'] = ports

      app_dir_path = os.path.dirname(os.path.dirname(service_dir_path))
      __with_no_publish(gateway_base, app_dir_path)
      __with_networks(gateway_base, hostnames) 

  with open(docker_compose_dest_path, 'w') as fp:
    yaml.dump(compose, fp) 

def __with_networks(config: dict, hostnames: List[str]):
  networks = {} 
  config['networks'] = networks
  networks[APP_EGRESS_NETWORK_NAME] = {}
  networks[APP_INGRESS_NETWORK_NAME] = {
    'aliases': hostnames
  }

def __with_no_publish(config: dict, app_dir_path: str):
  if not config['volumes']:
    config['volumes'] = []

  # Copy nginx.tmpl to .stoobly/tmp
  nginx_template_src_path = os.path.join(run_template_path(), GATEWAY_NGINX_TEMPLATE)
  nginx_template_relative_path = os.path.join(DATA_DIR_NAME, TMP_DIR_NAME, GATEWAY_NGINX_TEMPLATE)
  nginx_template_dest_path = os.path.join(app_dir_path, nginx_template_relative_path)

  if not os.path.exists(os.path.dirname(nginx_template_dest_path)):
    os.makedirs(os.path.dirname(nginx_template_dest_path), exist_ok=True)

  shutil.copy(nginx_template_src_path, nginx_template_dest_path)

  config['volumes'].append(
    f"{os.path.join(APP_DIR, nginx_template_relative_path)}:/app/nginx.tmpl:ro"
  )

  environment = {}
  if not config['environment']:
    config['environment'] = environment
  else:
    environment = config['environment']

  environment['HTTPS_METHOD'] = 'noredirect'

def __find_hosts(service_paths):
  hostnames = []
  ports = []
  for path in service_paths:
    config = ServiceConfig(path)

    if not config.hostname:
      continue

    try:
      port = int(config.port)
    except Exception:
      continue
    
    port_mapping = f"{port}:{port}"
    if port > 0 and port <= 65535 and port_mapping not in ports:
      ports.append(port_mapping)

    if config.hostname not in hostnames:
      hostnames.append(config.hostname) 

  return hostnames, ports