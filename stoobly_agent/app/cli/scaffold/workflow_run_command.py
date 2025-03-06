import dns.resolver
import os
import pdb
import subprocess
import re

from typing import TypedDict

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger

from .app import App
from .constants import (
  APP_NETWORK_ENV, CA_CERTS_DIR_ENV, CERTS_DIR_ENV, CONTEXT_DIR_ENV, NAMESERVERS_FILE, 
  SERVICE_DNS_ENV, SERVICE_NAME_ENV, USER_ID_ENV, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
)
from .docker.constants import DOCKERFILE_CONTEXT
from .workflow_command import WorkflowCommand
from .workflow_env import WorkflowEnv

LOG_ID = 'WorkflowRunCommand'

class ComposeOptions(TypedDict):
  namespace: str
  user_id: str

class BuildOptions(ComposeOptions):
  user_id: str
  verbose: bool

class DownOptions(ComposeOptions):
  extra_compose_path: str
  rmi: bool

class UpOptions(ComposeOptions):
  attached: bool
  extra_compose_path: str
  pull: bool

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__current_working_dir = os.getcwd()
    self.__ca_certs_dir_path = kwargs.get('ca_certs_dir_path') or app.ca_certs_dir_path
    self.__certs_dir_path = kwargs.get('certs_dir_path') or app.certs_dir_path
    self.__context_dir_path = kwargs.get('context_dir_path') or app.context_dir_path
    self.__network = kwargs.get('network') or self.app_config.network

  @property
  def ca_certs_dir_path(self):
    return self.__ca_certs_dir_path

  @property
  def certs_dir_path(self):
    return self.__certs_dir_path

  @property
  def context_dir_path(self):
    if not self.__context_dir_path:
      data_dir = DataDir.instance()
      return os.path.dirname(data_dir.path) 

    return self.__context_dir_path

  @property
  def current_working_dir(self):
    return self.__current_working_dir

  @current_working_dir.setter
  def current_working_dir(self, v):
    self.__current_working_dir = v

  @property
  def nameservers(self):
    path = self.nameservers_path
    if not os.path.exists(path):
      return []

    with open(path, 'r') as fp:
      nameservers = fp.read()
      return nameservers.split("\n")

  @property
  def nameservers_path(self):
    return os.path.join(self.app.data_dir.tmp_dir_path, NAMESERVERS_FILE)

  @property
  def network(self):
    return self.__network

  def create_image(self, **options: BuildOptions):
    relative_namespace_path = os.path.relpath(self.scaffold_namespace_path, self.__current_working_dir)
    dockerfile_path = os.path.join(relative_namespace_path, DOCKERFILE_CONTEXT)
    user_id = options['user_id'] or os.getuid()
    
    command = ['docker', 'build']
    command.append(f"-f {dockerfile_path}")
    command.append(f"-t stoobly.{user_id}")
    command.append(f"--build-arg USER_ID={user_id}")

    if not os.environ.get('STOOBLY_IMAGE_USE_LOCAL'):
      command.append('--pull')

    if not options.get('verbose'):
      command.append('--quiet')

    # To avoid large context transfer times, should be a folder with relatively low number of files
    command.append(relative_namespace_path) 

    return ' '.join(command)

  def remove_image(self, user_id: str = None):
    user_id = user_id or os.getuid()
    command = ['docker', 'rmi', f"stoobly.{user_id}", '&>', '/dev/null']
    command.append('|| true')
    return ' '.join(command)

  def create_network(self):
    return f"docker network create {self.network} &> /dev/null"

  def remove_network(self):
    return f"docker network rm {self.network} &> /dev/null || true"

  def up(self, **options: UpOptions):
    if not os.path.exists(self.compose_path):
      return ''

    command = ['COMPOSE_IGNORE_ORPHANS=true', 'docker', 'compose']
    command_options = []

    # Add docker compose file
    command_options.append(f"-f {os.path.relpath(self.compose_path, self.__current_working_dir)}")

    # Add custom docker compose file
    custom_services = self.custom_services
  
    if custom_services:
      uses_profile = False
      for service_name in custom_services:
        service = custom_services[service_name]
        profiles = service.get('profiles')
        if isinstance(profiles, list):
          if self.workflow_name in profiles:
            uses_profile = True
            break
      if not uses_profile:
        # TODO: looking into why warning does not print in docker
        Logger.instance(LOG_ID).error(f"Missing {self.workflow_name} profile in custom compose file")

      command_options.append(f"-f {os.path.relpath(self.custom_compose_path, self.__current_working_dir)}")

    if options.get('extra_compose_path'):
      command_options.append(f"-f {os.path.relpath(options['extra_compose_path'], self.__current_working_dir)}")

    command_options.append(f"--profile {self.workflow_name}") 

    if not options.get('namespace'):
      options['namespace'] = self.workflow_name
    command_options.append(f"-p {options['namespace']}")

    command += command_options
    command.append('up')

    if options.get('build'):
      command.append('--build')

    if options.get('pull'):
      command.append('--pull missing')

    if not options.get('attached'):
      command.append('-d')
    else:
      major_version = 2
      minor_version = 27
      patch_version = 0
      min_version = major_version * 10000 + minor_version * 100 + patch_version
      formula = "'{print $1*10000 + $2*100 + $3}'"
      option = f"$(test $(echo $(docker compose version --short) | awk -F. {formula}) -ge {min_version} && echo '--abort-on-container-failure')"

      # This option enables docker compose to return exit code 1 
      # when one of the services exits with a non-zero exit code
      # Otherwise, even if a service exits with a non-zero exit code, exit code 0 is returned
      command.append(option)

    self.write_env(**options)

    return ' '.join(command)

  def down(self, **options: DownOptions):
    if not os.path.exists(self.compose_path):
      return ''
  
    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {os.path.relpath(self.compose_path, os.getcwd())}")

    # Add custom docker compose file
    if self.custom_services:
      command.append(f"-f {os.path.relpath(self.custom_compose_path, self.__current_working_dir)}")

    if options.get('extra_compose_path'):
      command.append(f"-f {os.path.relpath(options['extra_compose_path'], self.__current_working_dir)}")

    command.append(f"--profile {self.workflow_name}") 

    if not options.get('namespace'):
      options['namespace'] = self.workflow_name
    command.append(f"-p {options['namespace']}")

    command.append('down')

    if options.get('rmi'):
      command.append('--rmi local')

    self.write_env(**options)

    return ' '.join(command)

  def write_nameservers(self):
    # If hostname is set then the service is external and we will need to configure the container's DNS.
    # If we don't configure the container's DNS, then Docker's embedded DNS will potentially
    # use configuration from the host's /etc/hosts file. The user may have configured their
    # /etc/hosts file to resolve requests to localhost
    #
    # See: 
    # https://forums.docker.com/t/docker-127-0-0-11-resolver-should-use-host-etc-hosts-file/55157
    # https://docs.docker.com/network/#dns-services
    # 
    # TODO: ideally we want to know if the service is built locally, if so, then no need to set DNS
    # since Docker's embedded DNS will resolve to it
    dns_resolver = dns.resolver.Resolver()

    with open(self.nameservers_path, 'w') as fp:
      nameservers = self.__find_nameservers(dns_resolver)
      ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$')
      nameservers = [ip for ip in nameservers if ipv4_pattern.match(ip)]
      if nameservers:
        fp.write("\n".join(nameservers))

  def write_env(self, **options: ComposeOptions):
    namespace = options.get('namespace')
    user_id = options.get('user_id')

    _config = {}
    _config[CA_CERTS_DIR_ENV] = self.ca_certs_dir_path
    _config[CERTS_DIR_ENV] = self.certs_dir_path
    _config[CONTEXT_DIR_ENV] = self.context_dir_path
    _config[SERVICE_NAME_ENV] = self.service_name
    _config[USER_ID_ENV] = user_id or os.getuid()
    _config[WORKFLOW_NAME_ENV] = self.workflow_name
    
    if namespace:
      _config[WORKFLOW_NAMESPACE_ENV] = namespace

    if self.network:
      _config[APP_NETWORK_ENV] = self.network

    nameservers = self.nameservers
    if nameservers:
      _config[SERVICE_DNS_ENV] = nameservers[0]

    env_vars = self.config(_config)
    WorkflowEnv(self.workflow_path).write(env_vars)
    return env_vars

  def __find_nameservers(self, dns_resolver: dns.resolver.Resolver):
    nameservers = dns_resolver.nameservers

    # If systemd-resolved is not used
    if nameservers != ['127.0.0.53']:
      return nameservers

    # Run the `resolvectl status` command and capture its output
    result = subprocess.run(['resolvectl', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if the command ran successfully
    if result.returncode != 0:
      return []

    # Extract the DNS servers using a regular expression
    #dns_servers = re.findall(r'DNS Servers: ([\d.]+(?:, [\d.]+)*)', result.stdout)
    pattern = re.compile('DNS Servers:(.*?)DNS Domain', re.DOTALL)
    match = re.findall(pattern, result.stdout)

    if not match:
      return []
      
    # Split the DNS servers string into a list
    dns_servers = match[0].strip().split("\n")
    return list(map(lambda dns_server: dns_server.strip(), dns_servers))
