import dns.resolver
import os
import pdb
import subprocess
import re

from stoobly_agent.config.data_dir import DataDir

from .app import App
from .constants import (
  APP_DIR_ENV, APP_NETWORK_ENV, CA_CERTS_DIR_ENV, CERTS_DIR_ENV, CONTEXT_DIR_ENV,
  SERVICE_DNS_ENV, SERVICE_NAME_ENV, SERVICE_SCRIPTS_DIR,  SERVICE_SCRIPTS_ENV, USER_ID_ENV,
  WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV, WORKFLOW_SCRIPTS_DIR, WORKFLOW_SCRIPTS_ENV, WORKFLOW_TEMPLATE_ENV
)

from .workflow_command import WorkflowCommand
from .workflow_env import WorkflowEnv
from .workflow_namesapce import WorkflowNamespace
from ..types.workflow_run_command import ComposeOptions

LOG_ID = 'WorkflowRunCommand'

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__app_dir_path = os.path.abspath(kwargs.get('app_dir_path') or app.dir_path)
    self.__current_working_dir = os.getcwd()
    self.__ca_certs_dir_path = kwargs.get('ca_certs_dir_path') or app.ca_certs_dir_path
    self.__certs_dir_path = kwargs.get('certs_dir_path') or app.certs_dir_path
    self.__containerized = kwargs.get('containerized') or False
    self.__context_dir_path = kwargs.get('context_dir_path') or app.context_dir_path
    self.__dry_run = kwargs.get('dry_run', False)
    self.__namespace = kwargs.get('namespace') or self.workflow_name
    self.__network = f"{self.__namespace}.{app.network}"
    self.__workflow_namespace = kwargs.get('workflow_namespace') or WorkflowNamespace(app, self.__namespace)

    self.__workflow_namespace.copy_dotenv()
    
  @property
  def app_dir_path(self):
    return self.__app_dir_path

  @property
  def ca_certs_dir_path(self):
    return self.__ca_certs_dir_path

  @property
  def certs_dir_path(self):
    return self.__certs_dir_path

  @property
  def containerized(self):
    return self.__containerized

  @property
  def context_dir_path(self):
    if not self.__context_dir_path:
      data_dir: DataDir = DataDir.instance()
      return os.path.dirname(data_dir.path) 

    return self.__context_dir_path

  @property
  def current_working_dir(self):
    return self.__current_working_dir

  @current_working_dir.setter
  def current_working_dir(self, v):
    self.__current_working_dir = v

  @property
  def dotenv_path(self):
    return self.__workflow_namespace.dotenv_path

  @property
  def dry_run(self):
    return self.__dry_run

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
    return self.__workflow_namespace.nameservers_path

  @property
  def namespace(self):
    return self.__namespace

  @property
  def network(self):
    return self.__network

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

  @property
  def workflow_namespace(self):
    return self.__workflow_namespace

  def write_env(self, **options: ComposeOptions):
    namespace = options.get('namespace')
    user_id = options.get('user_id')

    _config = {}
    _config[APP_DIR_ENV] = self.app_dir_path
    _config[CA_CERTS_DIR_ENV] = self.ca_certs_dir_path
    _config[CERTS_DIR_ENV] = self.certs_dir_path
    _config[CONTEXT_DIR_ENV] = self.context_dir_path
    _config[SERVICE_NAME_ENV] = self.service_name
    _config[SERVICE_SCRIPTS_ENV] = SERVICE_SCRIPTS_DIR
    _config[USER_ID_ENV] = user_id or os.getuid()
    _config[WORKFLOW_NAME_ENV] = self.workflow_name
    _config[WORKFLOW_SCRIPTS_ENV] = WORKFLOW_SCRIPTS_DIR
    _config[WORKFLOW_TEMPLATE_ENV] = self.workflow_name
    # Default to the workflow name if a namespace isn't given
    _config[WORKFLOW_NAMESPACE_ENV] = namespace if namespace else _config[WORKFLOW_NAME_ENV]

    if self.network:
      _config[APP_NETWORK_ENV] = self.network

    # Specified DNS should prioritized, otherwise defaults to internal DNS
    nameservers = self.nameservers
    if nameservers:
      _config[SERVICE_DNS_ENV] = nameservers[0]
    else:
      _config[SERVICE_DNS_ENV] = '8.8.8.8'

    env_vars = self.config(_config)
    WorkflowEnv(self.workflow_path).write(env_vars, self.dotenv_path)
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
