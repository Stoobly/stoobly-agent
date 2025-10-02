import os
from typing import List

from stoobly_agent.config.data_dir import DATA_DIR_NAME

from ...constants import (
  SERVICES_NAMESPACE, SERVICE_NAME, SERVICE_NAME_ENV, 
  STOOBLY_HOME_DIR, 
  WORKFLOW_NAME, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
)
from ...service_config import ServiceConfig

class ServiceBuilder():

  def __init__(self, config: ServiceConfig):
    self.__config = config
    self.__dir_path = config.dir
    self.__upstream_port = None
    self.__env = [SERVICE_NAME_ENV, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV]
    self.__service_name = os.path.basename(config.dir)
    self.__working_dir = os.path.join(
      STOOBLY_HOME_DIR, DATA_DIR_NAME, SERVICES_NAMESPACE, SERVICE_NAME, WORKFLOW_NAME
    )

  @property
  def config(self):
    return self.__config

  @property
  def dir_path(self):
    return self.__dir_path

  @property
  def upstream_port(self) -> int:
    return self.__upstream_port

  @property
  def service_name(self):
    return self.__service_name

  @property
  def working_dir(self):
    return self.__working_dir

  def env_dict(self):
    env = {}
    for e in self.__env:
      env[e] = '${' + e + '}'
    return env

  def with_upstream_port(self, v: int):
    if not isinstance(v, int):
      return self
    self.__upstream_port = v
    return self

  def with_env(self, v: List[str]): 
    if not isinstance(v, list):
      return self
    self.__env += v
    return self

  def write(self):
    """Base write method - to be implemented by subclasses"""
    pass
