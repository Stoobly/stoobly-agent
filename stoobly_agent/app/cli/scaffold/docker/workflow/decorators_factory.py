from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig

from ...constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from .detached_decorator import DetachedDecorator
from .dns_decorator import DnsDecorator
from .local_decorator import LocalDecorator
from .mock_decorator import MockDecorator
from .reverse_proxy_decorator import ReverseProxyDecorator

def get_workflow_decorators(workflow: str, service_config: ServiceConfig):
  workflow_decorators = []

  if workflow == WORKFLOW_RECORD_TYPE:
    if service_config.hostname:
      workflow_decorators.append(ReverseProxyDecorator)
      workflow_decorators.append(DnsDecorator)

      if service_config.local:
        workflow_decorators.append(LocalDecorator)
  elif workflow == WORKFLOW_MOCK_TYPE or workflow == WORKFLOW_TEST_TYPE:
     if service_config.hostname:
      workflow_decorators.append(DetachedDecorator if service_config.detached else MockDecorator)
      workflow_decorators.append(DnsDecorator)
  else:
    if service_config.hostname:
      workflow_decorators.append(DetachedDecorator if service_config.detached else MockDecorator) 

  return workflow_decorators