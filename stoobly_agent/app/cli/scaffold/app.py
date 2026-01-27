import hashlib
import os
import re
import shutil
from typing import TYPE_CHECKING

from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME

from .constants import SERVICES_NAMESPACE

if TYPE_CHECKING:
    from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace

class App():

  # path: path to the folder where data dir directory resides e.g. ~
  def __init__(self, path: str, **kwargs):
    path = os.path.abspath(path) or os.getcwd()
    data_dir: DataDir = DataDir.instance(path) 

    self.__containerized = kwargs.get('containerized', False)
    self.__data_dir = data_dir
    self.__data_dir_path = data_dir.path
    self.__dir_path = path
    self.__scaffold_namespace = kwargs.get('scaffold_namespace') or SERVICES_NAMESPACE
    self.__skip_validate_path = not not kwargs.get('dry_run')
    
    # Store host (kwarg) values
    self.__host_app_dir_path = kwargs.get('app_dir_path')
    self.__host_ca_certs_dir_path = kwargs.get('ca_certs_dir_path')
    self.__host_certs_dir_path = kwargs.get('certs_dir_path')
    self.__host_context_dir_path = kwargs.get('context_dir_path')
    self.__host_runtime_app_dir_path = self.__host_app_dir_path if self.__host_app_dir_path else None
    
    # If containerized, use data_dir/constructor values; otherwise use kwargs if provided
    if self.__containerized:
      self.__app_data_dir = DataDir.instance(path)
      self.__app_dir_path = path
      self.__ca_certs_dir_path = data_dir.ca_certs_dir_path
      self.__certs_dir_path = data_dir.certs_dir_path
      self.__context_dir_path = data_dir.context_dir_path
      self.__runtime_app_dir_path = self.__app_dir_path
    else:
      self.__app_data_dir = DataDir.instance(self.__host_app_dir_path or path)
      self.__app_dir_path = self.__host_app_dir_path or path
      self.__ca_certs_dir_path = self.__host_ca_certs_dir_path or data_dir.ca_certs_dir_path
      self.__certs_dir_path = self.__host_certs_dir_path or data_dir.certs_dir_path
      self.__context_dir_path = self.__host_context_dir_path or data_dir.context_dir_path
      self.__runtime_app_dir_path = self.__host_runtime_app_dir_path or self.__app_dir_path

  @property
  def app_data_dir(self):
    return self.__app_data_dir

  @property
  def app_dir_path(self):
    return os.path.abspath(self.__app_dir_path)

  @app_dir_path.setter
  def app_dir_path(self, v: str):
    self.__validate_path(v)
    self.__app_dir_path = v

  @property
  def ca_certs_dir_path(self):
    return os.path.abspath(self.__ca_certs_dir_path)

  @ca_certs_dir_path.setter
  def ca_certs_dir_path(self, v: str):
    self.__validate_path(v)
    self.__ca_certs_dir_path = v

  @property
  def certs_dir_path(self):
    return os.path.abspath(self.__certs_dir_path)

  @certs_dir_path.setter
  def certs_dir_path(self, v: str):
    self.__validate_path(v)
    self.__certs_dir_path = v

  @property
  def containerized(self):
    return self.__containerized

  @property
  def context_dir_path(self):
    return os.path.abspath(self.__context_dir_path)

  @context_dir_path.setter
  def context_dir_path(self, v: str):
    self.__validate_path(v)
    self.__context_dir_path = v 

  @property
  def data_dir(self):
    return self.__data_dir

  @property
  def data_dir_path(self):
    return os.path.join(self.context_dir_path, DATA_DIR_NAME)

  @property
  def host_app_dir_path(self):
    """Returns the host (kwarg) value for app_dir_path"""
    return os.path.abspath(self.__host_app_dir_path or self.app_dir_path)

  @property
  def host_ca_certs_dir_path(self):
    """Returns the host (kwarg) value for ca_certs_dir_path"""
    return os.path.abspath(self.__host_ca_certs_dir_path or self.ca_certs_dir_path)

  @property
  def host_certs_dir_path(self):
    """Returns the host (kwarg) value for certs_dir_path"""
    return os.path.abspath(self.__host_certs_dir_path or self.certs_dir_path)

  @property
  def host_context_dir_path(self):
    """Returns the host (kwarg) value for context_dir_path"""
    return os.path.abspath(self.__host_context_dir_path or self.context_dir_path)

  @property
  def host_runtime_app_dir_path(self):
    """Returns the host (kwarg) value for runtime_app_dir_path"""
    return os.path.abspath(self.__host_runtime_app_dir_path or self.runtime_app_dir_path)

  @property
  def valid(self):
    return os.path.exists(self.scaffold_namespace_path)

  @property
  def scaffold_namespace(self):
    return self.__scaffold_namespace

  @property
  def dir_path(self):
    return self.__dir_path

  @property
  def data_dir_path(self):
    return self.__data_dir_path

  @property
  def network(self):
    # An app may contain one or more context dirs from which services will derive their mocks from
    return hashlib.md5(self.host_context_dir_path.encode()).hexdigest()

  @property
  def runtime_app_dir_path(self):
    return os.path.abspath(self.__runtime_app_dir_path)

  @property
  def scaffold_namespace_path(self):
    return os.path.join(self.data_dir_path, self.scaffold_namespace)

  @property
  def services(self):
    return list(map(lambda path: os.path.basename(path), self.service_paths))

  @property
  def service_paths(self):
    services_dir = os.path.join(self.data_dir_path, self.scaffold_namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(path)

    return services

  def copy_folders_and_hidden_files(self, src: str, dst: str, ignore: list = []):
      os.makedirs(dst, exist_ok=True)

      # Walk through the source directory
      for root, dirs, files in os.walk(src):
          # Copy hidden files only
          for file_name in files:
              src_file_path = os.path.join(root, file_name)

              ignored = False

              # Skip files that match the ignore list pattern, use regex
              for ignore_pattern in ignore:
                  if re.fullmatch(os.path.join(src, ignore_pattern), src_file_path):
                      ignored = True
                      break

              if ignored:
                continue

              dst_file_path = os.path.join(dst, os.path.relpath(root, src), file_name)

              if not file_name.startswith('.'):
                  if os.path.exists(dst_file_path):
                      continue

              os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)  # Create directories in destination
              shutil.copy2(src_file_path, dst_file_path)

  def denormalize(self, workflow_namespace: 'WorkflowNamespace', migrate: bool = False):
    """
    Denormalize the app to the workflow namespace path.
    CA certs and certs dirs are not denormalized.
    """
    from stoobly_agent.app.cli.scaffold.denormalize_service import DenormalizeService
    denormalize_service = DenormalizeService(workflow_namespace)

    relative_path = os.path.relpath(workflow_namespace.path, self.app_dir_path)

    self.__runtime_app_dir_path = os.path.join(self.app_dir_path, relative_path)
    self.__host_runtime_app_dir_path = os.path.join(self.host_app_dir_path, relative_path)

    if migrate:
      return denormalize_service.denormalize()

    return True

  def __validate_path(self, v: str):
    if not isinstance(v, str):
      raise TypeError('Expected a str')

    if not self.__skip_validate_path:
      if not os.path.exists(v):
        raise ValueError(f"{v} does not exist")