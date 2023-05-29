import pdb

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.config.constants import test_filter
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse

class EndpointFacade():

  def __init__(self, endpoints_resource: EndpointsResource, endpoint_id: int):
    self.__endpoints_resource = endpoints_resource
    self.__endpoint_id = endpoint_id
    
    self.trace = None
    self.filter = test_filter.ALL

    # Cache
    self.__cached_body_param_names = None
    self.__cached_endpoint_show_response = None
    self.__cached_header_names = None
    self.__cached_query_param_names = None
    self.__cached_response_param_names = None

  def get(self) -> EndpointShowResponse:
    if self.__cached_endpoint_show_response:
      return self.__cached_endpoint_show_response

    endpoint_id = self.__endpoint_id
    resource = self.__endpoints_resource

    if not resource or not endpoint_id:
      return 

    try:
      res = resource.show(
        endpoint_id,
        aliases=True, 
        header_names=True,
        query_param_names=True,
        body_param_names=True,
        response_param_names=True
      )
    except Exception as e:
      return 

    if not res.ok:
      return 

    self.__cached_endpoint_show_response: EndpointShowResponse = res.json()

    return self.__cached_endpoint_show_response

  def with_show_response(self, res: EndpointShowResponse):
    self.__cached_endpoint_show_response = res
    return self

  @property
  def aliases(self):
    endpoint_show_response: EndpointShowResponse = self.get()
    return endpoint_show_response.get('aliases', [])

  @property
  def header_names(self) -> RequestComponentNamesFacade:
    if self.__cached_header_names:
      return self.__cached_header_names

    self.__cached_header_names = self.__request_component_names('header_names')

    return self.__cached_header_names

  @property
  def query_param_names(self) -> RequestComponentNamesFacade:
    if self.__cached_query_param_names:
      return self.__cached_query_param_names

    self.__cached_query_param_names = self.__request_component_names('query_param_names')

    return self.__cached_query_param_names

  @property
  def body_param_names(self) -> RequestComponentNamesFacade:
    if self.__cached_body_param_names:
      return self.__cached_body_param_names

    self.__cached_body_param_names = self.__request_component_names('body_param_names')

    return self.__cached_body_param_names

  @property
  def response_param_names(self) -> RequestComponentNamesFacade:
    if self.__cached_response_param_names:
      return self.__cached_response_param_names

    self.__cached_response_param_names = self.__request_component_names('response_param_names')

    return self.__cached_response_param_names

  def __request_component_names(self, component_name):
    endpoint_show_response: EndpointShowResponse = self.get()
    aliases = self.aliases
    component_names = endpoint_show_response.get(component_name) or []

    return RequestComponentNamesFacade(
      component_names      
    ).with_aliases(aliases).with_filter(self.filter).with_trace(self.trace)
