import pdb

from runpy import run_path
from typing import Callable

from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.app.settings import Settings

from .openapi_endpoint_adapter import OpenApiEndpointAdapter

class EndpointsApplyContext:

  def __init__(self):
    self.endpoints = []
    self.endpoint_handlers  = []
    self.lifecycle_hooks = {}
    self.request_handlers = []
    self.request_model = None
    self.scenario_id = None

  def with_endpoint_handler(self, handler: Callable[[EndpointShowResponse], None]):
    self.endpoint_handlers.append(handler)
    return self

  def with_lifecycle_hooks_path(self, path: str):
    try:
      self.lifecycle_hooks = run_path(path)
    except Exception as e:
      pass
  
    return self

  def with_project(self, project_id: int):
    settings = Settings.instance()

    resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)
    res = resource.index(project_id=project_id, ignored_components=1)
    res.raise_for_status()  
    
    self.endpoints += res.json()

    return self

  def with_request_handler(self, handler: Callable[[Request, EndpointShowResponse], None]):
    self.request_handlers.append(handler)
    return self

  def with_request_model(self, model):
    self.request_model = model
    return self

  def with_scenario(self, scenario_id: int):
    self.scenario_id = scenario_id
    return self

  def with_source(self, path: str, format: str):
    if format == OPENAPI_FORMAT:
      endpoint_adapter = OpenApiEndpointAdapter()
      self.endpoints += endpoint_adapter.adapt_from_file(path)

    return self