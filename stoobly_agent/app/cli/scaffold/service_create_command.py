import os
import pathlib
import shutil

from .constants import SERVICE_APPLICATION_TYPE, SERVICE_EXTERNAL_TYPE, SERVICE_SIDECAR_TYPE, SERVICE_TEMPLATE_VARIABLE, WORKFLOW_TEMPLATE_VARIABLE
from .config import Config
from .service_command import ServiceCommand

class ServiceCreateCommand(ServiceCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__force = not not kwargs.get('force')
    self.__hostname = kwargs.get('hostname')
    self.__port = kwargs.get('port')
    self.__scheme = kwargs.get('scheme')
    self.__service_name = kwargs['service_name']
    self.__type = kwargs.get('type') or SERVICE_APPLICATION_TYPE

    self.__templates_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'templates', 'service')

  @property
  def application_template_path(self):
    return os.path.join(self.__templates_dir, 'application')


  @property
  def external_template_path(self):
    return os.path.join(self.__templates_dir, 'external')

  @property
  def force(self):
    return self.__force

  @property
  def hostname(self):
    return self.__hostname

  @property
  def port(self):
    return self.__port

  @property
  def scheme(self):
    return self.__scheme

  @property
  def sidecar_template_path(self):
    return os.path.join(self.__templates_dir, 'sidecar')

  @property
  def service_name(self):
    return self.__service_name

  @property
  def type(self):
    return self.__type

  def build_with_docker(self):
    self.as_docker()
    dest = self.service_path

    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if self.type == SERVICE_APPLICATION_TYPE:
      shutil.copytree(self.application_template_path, dest, dirs_exist_ok=True)
    elif self.type == SERVICE_EXTERNAL_TYPE:
      shutil.copytree(self.external_template_path, dest, dirs_exist_ok=True)
    elif self.type == SERVICE_SIDECAR_TYPE:
      shutil.copytree(self.sidecar_template_path, dest, dirs_exist_ok=True)
    else:
      return

    self.write_config()
    self.format(self.service_path, self.__format_handler)
    
  def write_config(self):
    config = {}

    if self.hostname:
      config['SERVICE_HOSTNAME'] = self.hostname
    
    if self.port:
      config['SERVICE_PORT'] = self.port

    if self.scheme:
      config['SERVICE_SCHEME'] = self.scheme

    config_path = self.service_config_path
    Config(config_path).write(config)

  def __format_handler(self, path: str, contents: str):
    workflow_name = os.path.basename(os.path.dirname(path))
    contents = contents.replace(SERVICE_TEMPLATE_VARIABLE, self.service_name)
    return contents.replace(WORKFLOW_TEMPLATE_VARIABLE, workflow_name)