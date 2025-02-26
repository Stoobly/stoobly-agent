from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig

from ...constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE
from .development_decorator import DevelopmentDecorator
from .mock_decorator import MockDecorator
from .reverse_proxy_decorator import ReverseProxyDecorator

def get_workflow_decorators(workflow: str, service_config: ServiceConfig):
  workflow_decorators = []

  if workflow == WORKFLOW_RECORD_TYPE:
    if service_config.hostname:
      workflow_decorators.append(ReverseProxyDecorator)
      workflow_decorators.append(DevelopmentDecorator)
  elif workflow == WORKFLOW_MOCK_TYPE:
     if service_config.hostname:
      workflow_decorators.append(ReverseProxyDecorator if service_config.detached else MockDecorator)    
      workflow_decorators.append(DevelopmentDecorator)
  else:
    if service_config.hostname:
      workflow_decorators.append(ReverseProxyDecorator if service_config.detached else MockDecorator) 

  return workflow_decorators