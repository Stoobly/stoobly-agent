import copy
import pdb
from urllib.parse import parse_qs, urlencode
from urllib.parse import urlparse

from stoobly_agent.app.models.endpoint_model import EndpointModel
from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.models.types import EndpointCreateParams, OPENAPI_FORMAT
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings import Settings

class EndpointFacade():
  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.__endpoint_model = EndpointModel()
    self.local_db_request_adapter = RequestResourceFactory(self.__settings.remote).local_db()
  
  def create(self, **kwargs: EndpointCreateParams):
    if kwargs.get('format') == OPENAPI_FORMAT:
      self.__create_from_openapi(kwargs.get('endpoints'))

  # def __create_from_openapi(self, endpoints: str):
  def __create_from_openapi(self, file_path: str):
    open_api_spec = self.__endpoint_model.validate_and_parse(file_path=file_path)
    endpoints = self.__endpoint_model.adapt_openapi_endpoints(open_api_spec)

    for endpoint in endpoints:
      host = endpoint['host']
      if host == '':
        host = '%'
      port = endpoint['port']
      method = endpoint['method']
      pattern = endpoint['match_pattern']
      url = endpoint.get('url', '')
      endpoint_body = endpoint.get('body')

      params = RequestFindParams(host=host, port=port, method=method, pattern=pattern)
      similar_requests = self.local_db_request_adapter.find_similar_requests(params)

      # For each request, check contract
      # for request in similar_requests:
      #   continue
    return
 
