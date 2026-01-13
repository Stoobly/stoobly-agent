import os
import pdb
import yaml

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
  from stoobly_agent.app.cli.scaffold.docker.workflow.run_command import DockerWorkflowRunCommand

from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.run import iter_commands, run_options
from stoobly_agent.app.cli.scaffold.constants import APP_DIR, PROXY_MODE_REVERSE
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.docker.constants import APP_INGRESS_NETWORK_NAME, APP_EGRESS_NETWORK_NAME, DOCKER_COMPOSE_BASE, DOCKER_COMPOSE_BASE_TEMPLATE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME
from stoobly_agent.app.cli.scaffold.workflow_namesapce import WorkflowNamespace

class GatewayBase():

  def __init__(self, workflow_namespace: WorkflowNamespace, service_paths: List[str]):
    self.app_config: AppConfig = None
    self.commands: List['DockerWorkflowRunCommand'] = []
    self.log_level = None
    self.no_publish = False
    self.service_paths = service_paths
    self.workflow_namespace = workflow_namespace

  @property
  def app_dir_path(self):
    return os.path.dirname(os.path.dirname(self.service_dir_path))

  @property
  def proxy_mode(self):
    if not self.app_config:
      raise ValueError("App config is required")

    return self.app_config.proxy_mode

  @property
  def service_dir_path(self):
    if not self.service_paths:
      return None

    return os.path.dirname(self.service_paths[0])

  def with_app_config(self, app_config: AppConfig):
    self.app_config = app_config
    return self

  def with_commands(self, commands: List['DockerWorkflowRunCommand']):
    self.commands = commands
    return self

  def with_networks(self, hostnames: List[str], compose: dict):
    networks = {} 
    compose['networks'] = networks
    networks[APP_EGRESS_NETWORK_NAME] = {}
    networks[APP_INGRESS_NETWORK_NAME] = {
      'aliases': hostnames
    }
    return self

  def configure(self):
    if len(self.service_paths) == 0:
      return

    gateway_service_path = os.path.join(self.service_dir_path, CORE_GATEWAY_SERVICE_NAME)
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
        if self.proxy_mode == PROXY_MODE_REVERSE:
          hostnames, ports = self.__find_hosts()
        else:
          hostnames = [CORE_GATEWAY_SERVICE_NAME]

          if self.app_config:
            ports = [
              f"{self.app_config.proxy_port}:{self.app_config.proxy_port}",
            ]

        if not self.no_publish:
          gateway_base['ports'] = ports

        if self.proxy_mode == PROXY_MODE_REVERSE:
          self.with_traefik_config(gateway_base)
        else:
          self.with_run_options(gateway_base)

        self.with_networks(hostnames, gateway_base) 

    with open(docker_compose_dest_path, 'w') as fp:
      yaml.dump(compose, fp) 

  def with_run_options(self, compose: dict):
    def handle_before_entrypoint(public_directory_paths, response_fixtures_paths):
      options = run_options(
        self.app_config,
        public_directory_paths=public_directory_paths,
        response_fixtures_paths=response_fixtures_paths,
      )
      compose['command'] = options

    # Iterate through commands and add run options to the compose command
    iter_commands(
      self.commands,
      containerized=True,
      handle_before_entrypoint=handle_before_entrypoint
    )

  def __to_traefik_log_level(self):
    log_level = self.log_level

    if log_level == 'debug':
      log_level = 'DEBUG'
    elif log_level == 'warning':
      log_level = 'WARN'
    elif log_level == 'error':
      log_level = 'ERROR'
    else:
      log_level = 'INFO'

    return log_level

  def with_traefik_config(self, compose: dict):
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
        'level': self.__to_traefik_log_level(),
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

    for path in self.service_paths:
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
    traefik_template_relative_path = self.workflow_namespace.traefik_config_relative_path(self.app_dir_path)
    traefik_template_dest_path = self.workflow_namespace.traefik_config_path

    if not os.path.exists(os.path.dirname(traefik_template_dest_path)):
      os.makedirs(os.path.dirname(traefik_template_dest_path), exist_ok=True)

    with open(traefik_template_dest_path, 'w') as fp:
      fp.write(yaml.dump(traefik_config))

    compose['volumes'].append(
      f"{os.path.join(APP_DIR, traefik_template_relative_path)}:{config_dest}:ro"
    )

  def __find_hosts(self):
    hostnames = []
    ports = []
    for path in self.service_paths:
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