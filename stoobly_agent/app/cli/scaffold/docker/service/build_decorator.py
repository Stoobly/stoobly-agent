import pdb

from typing import TypedDict

from ...constants import DOCKER_NAMESPACE
from ..constants import DOCKERFILE_SERVICE
from .builder import ServiceBuilder
from .types import BuildDecoratorOptions

class BuildDecorator():

  def __init__(self, service_builder: ServiceBuilder):
    self.__service_builder = service_builder

  def decorate(self, **kwargs: BuildDecoratorOptions):
    service_builder = self.__service_builder
    build = {
      'context': '../..', # Assumes app root is 2 levels up
      'dockerfile': f"./{DOCKER_NAMESPACE}/{service_builder.service_name}/{DOCKERFILE_SERVICE}"
    }

    if 'build_args' in kwargs:
      args = {}
      for arg in kwargs['build_args']:
        args[arg] = '${' + arg + '}'
      build['args'] = args

    services = self.__service_builder.services
    app_name = self.__service_builder.app_base
    app_service = services.get(app_name) or {}

    services[app_name] = { 
      **app_service,
      **{ 
          'build': build,
        } 
    }