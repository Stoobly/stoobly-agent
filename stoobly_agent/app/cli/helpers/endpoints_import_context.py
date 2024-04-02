from typing import Callable, TypedDict

from .openapi_endpoint_adapter import OpenApiEndpointAdapter
from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.lib.api.body_param_names_resource import BodyParamNamesResource
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.header_names_resource import HeaderNamesResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.api.query_param_names_resource import QueryParamNamesResource
from stoobly_agent.lib.api.response_param_names_resource import ResponseParamNamesResource
from stoobly_agent.lib.api.response_header_names_resource import ResponseHeaderNamesResource

class EndpointsImportContext:
  def __init__(self):
    self.endpoints = []
    self.endpoint_handlers = []
    self.resources = {}
    self.project_id = None

  def with_endpoint_handler(self, handler: Callable[[EndpointShowResponse], None]):
    self.endpoint_handlers.append(handler)
    return self
  
  def with_project(self, project_id: int):
    self.project_id = project_id
    return self
  
  def with_endpoint_resource(self, resource: EndpointsResource):
    self.resources['endpoint'] = resource
    return self
  
  def with_header_name_resource(self, resource: HeaderNamesResource):
    self.resources['header_name'] = resource
    return self

  def with_body_param_name_resource(self, resource: BodyParamNamesResource):
    self.resources['body_param_name'] = resource
    return self

  def with_query_param_name_resource(self, resource: QueryParamNamesResource):
    self.resources['query_param_name'] = resource
    return self

  def with_response_param_name_resource(self, resource: ResponseParamNamesResource):
    self.resources['response_param_name'] = resource
    return self
  
  def with_response_header_name_resource(self, resource: ResponseHeaderNamesResource):
    self.resources['response_header_name'] = resource
    return self

  def with_source(self, path: str, format: str):
    if format == OPENAPI_FORMAT:
      endpoint_adapter = OpenApiEndpointAdapter()
      self.endpoints += endpoint_adapter.adapt_from_file(path)

    return self