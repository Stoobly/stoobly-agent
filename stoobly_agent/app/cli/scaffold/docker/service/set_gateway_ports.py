import os
import pdb
import yaml

from typing import List

from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.docker.constants import DOCKER_COMPOSE_BASE
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

    if port > 0 and port <= 65535 and port not in ports:
      ports.append(port)

  app_dir_path = os.path.dirname(service_paths[0])
  gateway_service_path = os.path.join(app_dir_path, CORE_GATEWAY_SERVICE_NAME)
  docker_compose_path = os.path.join(gateway_service_path, DOCKER_COMPOSE_BASE)

  with open(docker_compose_path, 'r+') as fp:
    compose = yaml.safe_load(fp)
    services = compose.get('services')

    if not services:
      return
    
    gateway_base = services.get('gateway_base')

    if not gateway_base:
      return

    gateway_base['ports'] = list(map(lambda port: f"{port}:{port}", ports))

    fp.seek(0)
    yaml.dump(compose, fp)
    fp.truncate()