import os
import pdb
import yaml

from typing import List

from stoobly_agent.app.cli.scaffold.constants import APP_DIR
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.docker.constants import APP_INGRESS_NETWORK_NAME, APP_EGRESS_NETWORK_NAME, DOCKER_COMPOSE_BASE, DOCKER_COMPOSE_BASE_TEMPLATE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME
from stoobly_agent.app.cli.scaffold.workflow_namesapce import WorkflowNamespace

def configure_gateway(workflow_namespace: WorkflowNamespace, service_paths: List[str], no_publish = False):
  if len(service_paths) == 0:
    return

  hostnames, ports = __find_hosts(service_paths)

  service_dir_path = os.path.dirname(service_paths[0])
  gateway_service_path = os.path.join(service_dir_path, CORE_GATEWAY_SERVICE_NAME)
  docker_compose_src_path = os.path.join(gateway_service_path, DOCKER_COMPOSE_BASE_TEMPLATE)
  docker_compose_dest_path = os.path.join(gateway_service_path, DOCKER_COMPOSE_BASE)

  if not os.path.exists(docker_compose_src_path):
    return

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
      __with_traefik_config(workflow_namespace, service_paths, app_dir_path, gateway_base)
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

def __with_traefik_config(workflow_namespace: WorkflowNamespace, service_paths: List[str], app_dir_path: str, compose: dict):
  config_dest = '/etc/traefik/traefik.yml'

  if not compose['volumes']:
    compose['volumes'] = []

  entry_points = {}
  certificates = []
  traefik_config = {
    'accessLog': {
      'format': 'common',
    },
    'entryPoints': entry_points,
    'log': {
      'format': 'common',
      'level': 'INFO',
    },
    'providers': {
      'docker': {
        'exposedByDefault': False
      },
      'file': {
        'fileName': config_dest,
        'watch': False
      }
    },
    'tls': {
      'certificates': certificates,
    },
  }

  for path in service_paths:
    config = ServiceConfig(path)

    if not config.hostname:
      continue

    entry_points[str(config.port)] = {
      'address': f":{config.port}"
    }

    if config.scheme == 'https':
      certificates.append({
        'certFile': f"/certs/{config.hostname}.crt",
        'keyFile': f"/certs/{config.hostname}.key",
      })

  # Create traefik.yml in .stoobly/tmp
  traefik_template_relative_path = workflow_namespace.traefik_config_relative_path(app_dir_path)
  traefik_template_dest_path = workflow_namespace.traefik_config_path

  if not os.path.exists(os.path.dirname(traefik_template_dest_path)):
    os.makedirs(os.path.dirname(traefik_template_dest_path), exist_ok=True)

  with open(traefik_template_dest_path, 'w') as fp:
    fp.write(yaml.dump(traefik_config))

  compose['volumes'].append(
    f"{os.path.join(APP_DIR, traefik_template_relative_path)}:{config_dest}:ro"
  )

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