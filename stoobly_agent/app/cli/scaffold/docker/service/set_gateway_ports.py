import os
import pdb
import yaml

from typing import List

from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.docker.constants import DOCKER_COMPOSE_BASE, DOCKER_COMPOSE_BASE_TEMPLATE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME

def set_gateway_ports(service_paths: List[str]):
  if len(service_paths) == 0:
    return

  ports = []
  for path in service_paths:
    config = ServiceConfig(path)

    try:
      port = int(config.port)
    except Exception:
      continue
    
    port_mapping = f"{port}:{443 if config.scheme == 'https' else 80}"
    if port > 0 and port <= 65535 and port_mapping not in ports:
      ports.append(port_mapping)

  app_dir_path = os.path.dirname(service_paths[0])
  gateway_service_path = os.path.join(app_dir_path, CORE_GATEWAY_SERVICE_NAME)
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
      gateway_base['ports'] = ports

  with open(docker_compose_dest_path, 'w') as fp:
    yaml.dump(compose, fp)