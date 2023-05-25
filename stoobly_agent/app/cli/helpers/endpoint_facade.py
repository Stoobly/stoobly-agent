import pdb

from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.models.types import EndpointCreateParams, OPENAPI_FORMAT
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.app.settings import Settings

from .openapi_endpoint_adapter import OpenApiEndpointAdapter
from .synchronize_request_service import synchronize_request

class EndpointFacade():
  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.local_db_request_adapter = RequestResourceFactory(self.__settings.remote).local_db()
  
  def create(self, **kwargs: EndpointCreateParams):
    if kwargs.get('format') == OPENAPI_FORMAT:
      self.__create_from_openapi(kwargs.get('endpoints'))

  def __create_from_openapi(self, file_path: str):
    endpoint_adapter = OpenApiEndpointAdapter()
    endpoints = endpoint_adapter.adapt_from_file(file_path)

    for endpoint in endpoints:
      host = endpoint['host']
      if host == '':
        host = '%'

      port = endpoint['port']
      method = endpoint['method']
      pattern = endpoint['match_pattern']

      params = RequestFindParams(host=host, port=port, method=method, pattern=pattern)
      similar_requests = self.local_db_request_adapter.find_similar_requests(params)

      for request in similar_requests:
        synchronize_request(request, endpoint)